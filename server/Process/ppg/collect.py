import websockets
import asyncio
import pymysql
import datetime


async def hello(websocket,path):
    global conn,cursor,date
    sql_hr="insert into hr_{date} values(%s,%s,%s)".format(date=date)
    sql_ppg="insert into ppg_{date} values(%s,%s)".format(date=date)
    while True:
        data = await websocket.recv()
        ppg=data[:64]
        heartrate=data[64]
        spo2=data[65]
        cursor.execute(sql_hr,(datetime.datetime.now().strftime('%H:%M:%S'),heartrate,spo2))
        for data in ppg:
            cursor.execute(sql_ppg,(datetime.datetime.now().strftime('%H:%M:%S'),data))
        conn.commit()


def seupDatabase():
    global conn,cursor,date
    conn = pymysql.connect(host='127.0.0.1', user='root', password='pi', database='ppg')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    date=datetime.datetime.now().strftime('%Y_%m_%d')
    try:
        cursor.execute("create table hr_%s(time varchar(10), heartrate int, spo2 int)"%date)
        cursor.execute("create table ppg_%s(time varchar(10), ppg int)"%date)
    except Exception as err:
        print("Table Existed!")



seupDatabase()

start_server = websockets.serve(hello,'0.0.0.0',7891)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
