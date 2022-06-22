import bluetooth
import time
target_add='98:DA:60:02:6B:36'
s=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((target_add,1))
print('Connected')
i,j,k=0,0,0
num=1
while True:
    light=(i).to_bytes(1,byteorder='big')+(j).to_bytes(1,byteorder='big')+(k).to_bytes(1,byteorder='big')
    s.send(light)
    
    i+=1*num
    if i==255 or i==0:
        num=-num
    time.sleep(0.01)
        
#s.send(b'\x00\x00\x00')
