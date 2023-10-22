# main.py
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.websockets import WebSocketState
#import databases
#import sqlalchemy
#from databases import Database
import uvicorn
import pandas as pd
from clickhouse_driver import Client
from pydantic import BaseModel
from fastapi import HTTPException
import json
from datetime import datetime
import time
from fastapi.routing import APIRoute
from fastapi.templating import Jinja2Templates


client = Client(host='75.119.142.124', port=9035, user='default', password='qolkasw10-=', database='default')

# FastAPI setup
app = FastAPI()
templates = Jinja2Templates(directory="templates")

df = pd.DataFrame(columns=['status', 'id_forklift', 'id_warehouse', 'id_task', 'id_point', 'event_timestamp','last_service_date'])

query = """
SELECT id_forklift,id_warehouse,id_point
FROM (
    SELECT *,
           max(event_timestamp) OVER (PARTITION BY id_forklift, id_warehouse) AS max_event_timestamp
    FROM default.main_data_stg
) AS subquery
WHERE event_timestamp = max_event_timestamp
"""

# Выполните запрос и получите результат
result = client.execute(query)
current_dic = {str((x, y)): value for x, y, value in result}


time_all=0
active_connections = []
dict_active_connections = {}

async def send_updated_data(new_data):
    global current_dic
    global active_connections

    selected_columns = new_data[['id_forklift', 'id_warehouse', 'id_point']]
    selected_columns['key'] = selected_columns.apply(lambda row: f'({row["id_forklift"]},{row["id_warehouse"]})', axis=1)

    # Преобразуем в словарь
    result_dict = selected_columns.set_index('key')['id_point'].to_dict()
    #print('--------------------------------------------------------------------------------------')
    flag = False
    update_df = {}
    for i in result_dict:
        if (i in current_dic and result_dict[i]!=current_dic[i]) or (not i in current_dic):
            update_df[i] = str(result_dict[i])
            flag = True
        current_dic[i]=str(result_dict[i])


    if flag:
        json_str = json.dumps(update_df)
        print(len(active_connections))
        for connection in active_connections:
            await connection.send_text(json_str)

@app.websocket("/ws2")
async def websocket_endpoint2(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        json_str = json.dumps(current_dic)
        print('Send data')
        await websocket.send_text(json_str)
       
        print("Сообщение отправлено клиенту") 
        while True:  # Бесконечный цикл для приема сообщений
            message = await websocket.receive_text()
    except WebSocketDisconnect:
        # Соединение закрыто
        active_connections.remove(websocket)
    if len(active_connections)>0:
        print(websocket.state == WebSocketState.CONNECTED)
        print(active_connections[-1]==WebSocketState.CONNECTED)

start = time.time()
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global df
    global start
    await websocket.accept()
    file_csv = open('log.csv','a')

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"You sent: {data}")
            file_csv.write(data+'\n')
        # print(data)
            new_data = pd.DataFrame([dict(zip(df.columns,data.split(';')))])
            new_data1 = new_data.copy()
            await send_updated_data(new_data1)
            new_data['event_timestamp'] = pd.to_datetime(new_data['event_timestamp'], format='%Y-%m-%d %H:%M:%S.%f')
            new_data['last_service_date'] = pd.to_datetime(new_data['last_service_date'], format='%Y-%m-%d %H:%M:%S.%f')
            new_data['last_service_date'].fillna(pd.Timestamp.min, inplace=True)

            df = pd.concat([df, new_data], ignore_index=True)


            if (time.time() - start) > 10:
                start = time.time()
                df_insert = df.copy()
                df_insert['id_forklift'] = df_insert['id_forklift'].astype(int)
                df_insert['id_warehouse'] = df_insert['id_warehouse'].astype(int)
                df_insert['id_task'] = df_insert['id_task'].astype(int)
                file_csv.close()
                client.execute('INSERT INTO main_data_stg_t2 (status, id_forklift, id_warehouse, id_task, id_point, event_timestamp,last_service_date) VALUES', list(df_insert.itertuples(index=False, name=None)))
                selected_rows = df_insert[(df_insert['status'] == 'CHILL') | (df_insert['status'] == 'START')]
                selected_columns = selected_rows[['id_forklift', 'id_warehouse', 'last_service_date']]
                selected_columns = selected_columns.rename(columns={'last_service_date': 'last_maintenance_date','id_warehouse':'id_warehousr'})
                selected_columns['next_maintenance_date'] = selected_columns['last_maintenance_date'] + pd.Timedelta(days=181)
                client.execute('INSERT INTO maintenance_catalog (id_forklift, id_warehousr, last_maintenance_date, next_maintenance_date) VALUES', list(selected_columns.itertuples(index=False, name=None)))                    
                with open('log.csv', 'w') as file:
                        pass
                file_csv = open('log.csv','a')
                df = pd.DataFrame(columns=['status', 'id_forklift', 'id_warehouse', 'id_task', 'id_point', 'event_timestamp','last_service_date'])
                df = df.drop(df[df.isin(df_insert.to_dict('list')).all(axis=1)].index)
    except Exception as ex:
        print('Error----------------------------------------------',ex)
        file_csv.close()

def list_routes():
    routes = []
    for route in app.routes:
        if isinstance(route, APIRoute):
            routes.append({"path": route.path, "methods": route.methods})
    return routes

@app.get("/")
async def home(request: Request):
    routes = list_routes()
    return templates.TemplateResponse("routes_template.html", {"request":request, "routes": routes})
    

class LoaderInfo(BaseModel):
    id_forklift: int
    status: str
    id_task: int
    last_maintenance_date: datetime
    next_maintenance_date: datetime


@app.get("/forklift_info/{id_forklift}/{id_warehouse}")
async def get_loader_info(id_forklift: int, id_warehouse: int):
    # Выполните SQL-запрос к ClickHouse для извлечения информации
    query = f"""
        select 
        id_forklift, 
        CASE WHEN status in ('CHILL') THEN 'Жду заказ'
        WHEN status in ('START','WORK_UP') THEN 'Еду за заказом'
        WHEN status in ('TARGET','WORK_DOWN','FINISH') THEN 'Возвращаюсь с заказом'
        end as status,
        id_task,
        maint_dates as last_d,
        maint_dates + INTERVAL 181 DAY AS "Дата следующего ТО"
    from(
        SELECT  mds.id_forklift, mds.status, mds.id_task, 
                dictGet('maintenance_catalog_dict', 'last_maintenance_date', ({id_forklift}, {id_warehouse})) as maint_dates,
                mds.event_timestamp
                FROM default.main_data_stg mds
                WHERE mds.id_forklift = {id_forklift}
                order by event_timestamp desc
                limit 1
                );
                """
    
    try:
        result = client.execute(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    if not result:
        raise HTTPException(status_code=404, detail="Loader information not found")
    
    # Преобразуйте результат запроса в объект модели
    loader_info = LoaderInfo(
        id_forklift=result[0][0],
        status=result[0][1],
        id_task=result[0][2],
        last_maintenance_date=result[0][3],
        next_maintenance_date=result[0][4]
    )
    
    return loader_info
if __name__ == "__main__":

    uvicorn.run(app, host="75.119.142.124", port=8002)