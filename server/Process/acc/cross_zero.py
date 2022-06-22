import pymysql
import json
import datetime
import numpy as np
conn = pymysql.connect(host='127.0.0.1', user='root', password='pi', database='acc')
# cursor=pymysql.cursors.DictCursor,是为了将数据作为一个字典返回
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
date = datetime.datetime.now().date().strftime('%Y_%m_%d')

try:
    sql = 'select * from data_{date} ORDER BY time DESC LIMIT 1'.format(date=date)
    cursor.execute(sql)

except Exception as e:
    print(e)
    date = (datetime.datetime.now() + datetime.timedelta(days=-1)).date().strftime('%Y_%m_%d')
    sql = 'select * from data_{date} ORDER BY time DESC LIMIT 1'.format(date=date)
    cursor.execute(sql)

now_time = cursor.fetchall()[0]['time']
now_time=datetime.datetime.strptime(now_time,'%H:%M:%S')
win_unit=5
#len_list=[]
acc_list=[[],[],[],[],[]]
delta_angle_list=[[],[],[],[],[]]
#判断是否过了二十五秒？
for num in reversed(range(5)):
    time_list=[(now_time+datetime.timedelta(seconds=-i-num*win_unit)).strftime("%H:%M:%S") for i in reversed(range(win_unit))]
    #print(time_list)
    acc_list[num]=[]
    delta_angle_list[num]=[]
    for time in time_list:
        sql="select acc, delta_angle from data_{date} where time='{time}'".format(date=date,time=time)
        cursor.execute(sql)
        data = cursor.fetchall()
        for item in data:
            acc_list[num].append(item['acc'])
            delta_angle_list[num].append(item['delta_angle'])
        #len_list.append(len(data))

#计算过零率：
acc_standard=1
ang_standard=1
coef=5.52
zerocross_rate_acc=[0,0,0,0,0]
zerocross_rate_angle=[0,0,0,0,0]
for k in range(len(acc_list)):
    for i in range(len(acc_list[k])-1):
        zerocross_rate_acc[k]+=abs(np.sign(acc_list[k][i]-acc_standard)-np.sign(acc_list[k][i+1]-acc_standard))
        zerocross_rate_angle[k]+=abs(np.sign(delta_angle_list[k][i]-ang_standard)-np.sign(delta_angle_list[k][i+1]-ang_standard))

Z=coef*(0.06*(zerocross_rate_acc[0]+zerocross_rate_angle[0])+0.24*(zerocross_rate_acc[1]+zerocross_rate_angle[1])+(zerocross_rate_acc[2]+zerocross_rate_angle[2])+0.22*((zerocross_rate_acc[3]+zerocross_rate_angle[3]))+0.04*((zerocross_rate_acc[4]+zerocross_rate_angle[4])))
print(Z)
if Z>=1:
    print("wake")
else:
    print("Sleeping")
