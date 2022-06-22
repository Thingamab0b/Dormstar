from serial.tools import list_ports
import serial
import websockets
import asyncio
import sys
import time

          
ser = serial.Serial('/dev/ttyAMA0', 38400, timeout=1)
ser.timeout=2
if ser.isOpen():
    print("Connected!")
    ser.write('\x8a'.encode())#开机
    
async def Trans():
    global ser
    async with websockets.connect('ws://110.42.138.202:7891') as websocket:
        while True:
          #  s=time.time()
            data=ser.read(76)
           # print(time.time()-s)
            await websocket.send(data[1:67])
        
        
asyncio.get_event_loop().run_until_complete(Trans())
