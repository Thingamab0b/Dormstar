import websockets
import asyncio
from math import sqrt
import pymysql
import json
import datetime

global conn,cursor,date
global pre_angle_x,pre_angle_y,pre_angle_z
pre_angle_x,pre_angle_y,pre_angle_z=0,0,0

def get_acc(datahex):  
    axl = datahex[0]                                        
    axh = datahex[1]
    ayl = datahex[2]                                        
    ayh = datahex[3]
    azl = datahex[4]                                        
    azh = datahex[5]
    
    k_acc = 16.0
 
    acc_x = (axh << 8 | axl) / 32768.0 * k_acc
    acc_y = (ayh << 8 | ayl) / 32768.0 * k_acc
    acc_z = (azh << 8 | azl) / 32768.0 * k_acc
    if acc_x >= k_acc:
        acc_x -= 2 * k_acc
    if acc_y >= k_acc:
        acc_y -= 2 * k_acc
    if acc_z >= k_acc:
        acc_z-= 2 * k_acc
    
    return sqrt(acc_x**2+acc_y**2+acc_z**2) #合加速度


def get_delta_angle(datahex):   
    global pre_angle_x,pre_angle_y,pre_angle_z                          
    rxl = datahex[0]                                        
    rxh = datahex[1]
    ryl = datahex[2]                                        
    ryh = datahex[3]
    rzl = datahex[4]                                        
    rzh = datahex[5]
    k_angle = 180.0
 
    angle_x = (rxh << 8 | rxl) / 32768.0 * k_angle
    angle_y = (ryh << 8 | ryl) / 32768.0 * k_angle
    angle_z = (rzh << 8 | rzl) / 32768.0 * k_angle
    if angle_x >= k_angle:
        angle_x -= 2 * k_angle
    if angle_y >= k_angle:
        angle_y -= 2 * k_angle
    if angle_z >=k_angle:
        angle_z-= 2 * k_angle
    
    delta_angle=abs(angle_x-pre_angle_x)+abs(angle_z-pre_angle_z)+abs(angle_z-pre_angle_z)
    pre_angle_x,pre_angle_y,pre_angle_z=angle_x,angle_y,angle_z
    return delta_angle

def seupDatabase():
    global conn,cursor,date
    conn = pymysql.connect(host='127.0.0.1', user='root', password='pi', database='acc')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    date=datetime.datetime.now().strftime('%Y_%m_%d')
    try:
        cursor.execute("create table data_%s(time varchar(10), acc float, delta_angle float)"%date)
    except Exception as err:
        print("Table Existed!")

async def hello(websocket,path):
    global conn,cursor,date
    sql="insert into data_{date} values(%s,%s,%s)".format(date=date)
    while True:
         data = await websocket.recv() #6 bytes ax,ay,az,wx,wy,wz
         acc=get_acc(data[:6])
         delta_angle=get_delta_angle(data[6:])
         cursor.execute(sql,(datetime.datetime.now().strftime('%H:%M:%S'),acc,delta_angle))
         conn.commit()


seupDatabase()
start_server = websockets.serve(hello,'0.0.0.0',7890)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
