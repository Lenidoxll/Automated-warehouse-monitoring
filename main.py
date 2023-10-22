# main.py
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.websockets import WebSocketState
from fastapi.responses import FileResponse
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
from fastapi.staticfiles import StaticFiles
from pathlib import Path

client = Client(host='75.119.142.124', port=9035, user='default', password='qolkasw10-=', database='default')

# FastAPI setup
app = FastAPI()
templates = Jinja2Templates(directory="templates")
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

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
                file_csv.close() # Сохраняем файл с логами, если при запросе к БД ошибка - данные не потеряются
                selected_rows = df_insert[(df_insert['status'] == 'CHILL') | (df_insert['status'] == 'START')].copy()
                df_insert = df_insert.drop('last_service_date', axis=1)
                print(df_insert)
                client.execute('INSERT INTO main_data_stg (status, id_forklift, id_warehouse, id_task, id_point, event_timestamp) VALUES', list(df_insert.itertuples(index=False, name=None)))
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



class LoaderInfo(BaseModel):
    id_forklift: int
    status: str
    id_task: int
    last_maintenance_date: datetime
    next_maintenance_date: datetime

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


@app.get("/query1/{id_forklift}/{id_warehouse}/{from_ts}/{to_ts}")   # YYYY-MM-DD
async def get_loader_info(id_forklift: int, id_warehouse: int,from_ts,to_ts):
    dists = {'K1': {'K1': 0, 'K2': 5},
    'K2': {'K2': 0, 'K1': 5, 'K3': 10, 'K5': 5},
    'K3': {'K3': 0, 'K2': 10, 'X1': 10, 'K4': 15},
    'X1': {'X1': 0, 'K3': 10},
    'K4': {'K4': 0, 'K3': 15, 'X2': 10},
    'X2': {'X2': 0, 'K4': 10},
    'K5': {'K5': 0, 'K2': 5, 'K6': 10, 'K8': 5},
    'K6': {'K6': 0, 'K5': 10, 'X3': 10, 'K7': 15},
    'X3': {'X3': 0, 'K6': 10},
    'K7': {'K7': 0, 'K6': 15, 'X4': 10},
    'X4': {'X4': 0, 'K7': 10},
    'K8': {'K8': 0, 'K5': 5, 'K9': 10},
    'K9': {'K9': 0, 'K8': 10, 'X5': 5, 'K10': 15},
    'X5': {'X5': 0, 'K9': 5},
    'K10': {'K10': 0, 'K9': 15, 'X6': 10},
    'X6': {'X6': 0, 'K10': 10}}
    # Выполните SQL-запрос к ClickHouse для извлечения информации
    from_datetime = datetime.strptime(from_ts, "%Y-%m-%d")
    to_datetime = datetime.strptime(to_ts, "%Y-%m-%d")
    print(from_datetime,to_datetime)
    query = f"""
SELECT *
FROM `default`.main_data_stg
WHERE id_forklift = {id_forklift}
and id_warehouse =  {id_warehouse}
and event_timestamp BETWEEN '{from_datetime}' and '{to_datetime}'
ORDER by event_timestamp ASC ;
                """
    print(query)
    
    try:
        result = client.execute(query)
        if result ==[]:
            return {}
        df = pd.DataFrame(result, columns=[desc[0] for desc in client.execute("DESCRIBE `default`.main_data_stg")])
        df['dist'] = df.apply(lambda row: dists[row['id_point']][row['id_next_point']],axis=1)
        result = df['dist'].sum()
        print(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    if not result:
        raise HTTPException(status_code=404, detail="Loader information not found")


    return result


@app.get("/query2/{id_forklift}/{id_warehouse}/{from_ts}/{to_ts}")   # YYYY-MM-DD
async def get_loader_info(id_forklift: int,id_warehouse: int,from_ts,to_ts):
    # Выполните SQL-запрос к ClickHouse для извлечения информации
    from_datetime = datetime.strptime(from_ts, "%Y-%m-%d")
    to_datetime = datetime.strptime(to_ts, "%Y-%m-%d")
    print(from_datetime,to_datetime)
    query = f"""
SELECT COUNT(*)
FROM `default`.main_data_stg
WHERE id_forklift = {id_forklift} 
and id_warehouse =  {id_warehouse}
and event_timestamp BETWEEN '{from_datetime}' and '{to_datetime}'
and status = 'FINISH'
                """
    print(query)
    
    try:
        result = client.execute(query)
        if result ==[]:
            return {}
        print(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if not result:
        raise HTTPException(status_code=404, detail="Loader information not found")
    return result


@app.get("/query3/{id_forklift}/{id_warehouse}/{from_ts}/{to_ts}/{num}")   # YYYY-MM-DD
async def get_loader_info(id_forklift: int,id_warehouse: int,from_ts,to_ts,num: int):
    # Выполните SQL-запрос к ClickHouse для извлечения информации
    from_datetime = datetime.strptime(from_ts, "%Y-%m-%d")
    to_datetime = datetime.strptime(to_ts, "%Y-%m-%d")
    query = f"""
SELECT *
FROM `default`.main_data_stg
WHERE id_forklift = {id_forklift} 
and id_warehouse =  {id_warehouse}
and event_timestamp BETWEEN '{from_datetime}' and '{to_datetime}'
AND (status IN ('FINISH','START')) 
ORDER by event_timestamp ASC ;

                """
    
    try:
        result = client.execute(query)
        if result ==[]:
            return {}
        df = pd.DataFrame(result, columns=[desc[0] for desc in client.execute("DESCRIBE `default`.main_data_stg")])
        # leave only start/finish events. assume the rover moves all the time, while not on k1 station
        idle_time = (df['event_timestamp'] - df['event_timestamp'].shift(1)).sum() 
        if df['status'][0] == 'START':
            idle_time = (df['event_timestamp'] - df['event_timestamp'].shift(1))[1::2].sum()
        else:
            idle_time (df['event_timestamp'] - df['event_timestamp'].shift(1))[::2].sum()
        busy_time = df['event_timestamp'].max() - df['event_timestamp'].min() - idle_time
        if num==1:
            return busy_time   
        else:
            return idle_time
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if not result:
        raise HTTPException(status_code=404, detail="Loader information not found")
    return result

@app.get("/query4/{id_forklift}/{id_warehouse}/{from_ts}/{to_ts}")   # YYYY-MM-DD
async def get_loader_info(id_forklift: int,id_warehouse: int,from_ts,to_ts):
    # Выполните SQL-запрос к ClickHouse для извлечения информации
    from_datetime = datetime.strptime(from_ts, "%Y-%m-%d")
    to_datetime = datetime.strptime(to_ts, "%Y-%m-%d")
    print(from_datetime,to_datetime)
    query = f"""
SELECT *
FROM `default`.main_data_stg
WHERE id_forklift = {id_forklift} 
and id_warehouse =  {id_warehouse}
and event_timestamp BETWEEN '{from_datetime}' and '{to_datetime}'
ORDER by event_timestamp ASC ;

                """
    print(query)
    
    try:
        result = client.execute(query)
        if result ==[]:
            return {}
        df = pd.DataFrame(result, columns=[desc[0] for desc in client.execute("DESCRIBE `default`.main_data_stg")])
        resps = df[df['status'] != df['status'].shift()]
       # print(resps)
        resps['time_in_state'] = resps['event_timestamp'] - df['event_timestamp'].shift()
        result = resps.groupby(['status']).aggregate({'time_in_state': 'sum' })
        result['time_in_state'] = result['time_in_state'].apply(lambda x: str(x))
        #Преобразовать результат агрегации в словарь
        result = result.to_dict()
        print(result)
        result = json.dumps(result)

        # Преобразовать результат агрегации в JSON
        #result = result.to_json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
   # if not result:
    #    raise HTTPException(status_code=404, detail="Loader information not found")

    return result


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

@app.get("/canvas")
async def canvas(request: Request):
    return FileResponse(path="templates/index.html", media_type="text/html")

if __name__ == "__main__":

    uvicorn.run(app, host="75.119.142.124", port=8003)