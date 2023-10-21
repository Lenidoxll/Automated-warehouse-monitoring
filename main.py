# main.py
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
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


client = Client(host='75.119.142.124', port=9035, user='default', password='qolkasw10-=', database='default')

'''
DATABASE_URL = "sqlite:///./test.db"
database = Database(DATABASE_URL)

# SQLAlchemy setup
metadata = MetaData()
engine = create_engine(DATABASE_URL)
messages = Table(
    "messages",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("content", String),
)
'''

# FastAPI setup
app = FastAPI()

df = pd.DataFrame(columns=['status', 'id_forklift', 'id_warehouse', 'id_task', 'id_point', 'event_timestamp'])

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
print(current_dic)

k=0
'''
@app.on_event("startup")
async def startup_db_client():
    await database.connect()

@app.on_event("shutdown")
async def shutdown_db_client():
    await database.disconnect()
'''
active_connections = []

async def send_updated_data(new_data):
    global current_dic
    global active_connections

    selected_columns = new_data[['id_forklift', 'id_warehouse', 'id_point']]
    selected_columns['key'] = selected_columns.apply(lambda row: f'({row["id_forklift"]},{row["id_warehouse"]})', axis=1)

    # Преобразуем в словарь
    result_dict = selected_columns.set_index('key')['id_point'].to_dict()
    #print(result_dict)
    #print('--------------------------------------------------------------------------------------')
    flag = False
    for i in result_dict:
        if (i in current_dic and result_dict[i]!=current_dic[i]) or (not i in current_dic):
            flag = True
        current_dic[i]=str(result_dict[i])
       # print(current_dic[i],result_dict[i])


    if flag:
        json_str = json.dumps(current_dic)
        print(len(active_connections))
        for connection in active_connections:
            if connection.state == WebSocketState.CONNECTED:
                print('STATE???')
                await connection.send_text(json_str)
            else:
                print('Not Connected:', connection)

                print('NOT CONNECTED')


@app.websocket("/ws2")
async def websocket_endpoint2(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        json_str = json.dumps(current_dic)
        print('ОТПРАВИЛ???')
        await websocket.send_text(json_str)
       
        print("Сообщение отправлено клиенту")  # Добавьте эту строку для логирования
        while websocket.state == WebSocketState.CONNECTED:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        # Соединение закрыто
        print('СОЕДИНЕНИЕ ЗАКРЫТО')
        active_connections.remove(websocket)



@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global df
    global k
    await websocket.accept()
    
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"You sent: {data}")
       # print(data)
        new_data = pd.DataFrame([dict(zip(df.columns,data.split(';')))])
        new_data1 = new_data.copy()
        await send_updated_data(new_data1)
        new_data['event_timestamp'] = pd.to_datetime(new_data['event_timestamp'], format='%Y-%m-%d %H:%M:%S.%f')

        df = pd.concat([df, new_data], ignore_index=True)
       # print(df)
        k+=1
        if k%100 == 0:
            df_insert = df.copy()
            df_insert['id_forklift'] = df_insert['id_forklift'].astype(int)
            df_insert['id_warehouse'] = df_insert['id_warehouse'].astype(int)
            df_insert['id_task'] = df_insert['id_task'].astype(int)
            client.execute('INSERT INTO main_data_stg (status, id_forklift, id_warehouse, id_task, id_point, event_timestamp) VALUES', list(df_insert.itertuples(index=False, name=None)))
            df = pd.DataFrame(columns=['status', 'id_forklift', 'id_warehouse', 'id_task', 'id_point', 'event_timestamp'])
            df = df.drop(df[df.isin(df_insert.to_dict('list')).all(axis=1)].index)
            print('CUR_DF = ',df)


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
    select id_forklift, status, id_task, maint_dates.1 as last_d, maint_dates.2 as next_date from(
        SELECT  mds.id_forklift, mds.status, mds.id_task, 
                dictGet('maintenance_catalog_dict', ('last_maintenance_date', 'next_maintenance_date'), ({id_forklift}, {id_warehouse})) as maint_dates,
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

    uvicorn.run(app, host="75.119.142.124", port=8001)