import websockets
import asyncio
from math import sqrt
import pymysql
import json
import datetime


def get_hr_spo2():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='pi', database='ppg')
    # cursor=pymysql.cursors.DictCursor,是为了将数据作为一个字典返回
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    date = datetime.datetime.now().date().strftime('%Y_%m_%d')

    try:
        sql = 'select * from hr_{date} ORDER BY time DESC LIMIT 1'.format(date=date)
        cursor.execute(sql)
    except Exception as e:
        print(e)
        date = (datetime.datetime.now() + datetime.timedelta(days=-1)).date().strftime('%Y_%m_%d')
        sql = 'select * from hr_{date} ORDER BY time DESC LIMIT 1'.format(date=date)
        cursor.execute(sql)

    data=cursor.fetchall()[0]
    return data
