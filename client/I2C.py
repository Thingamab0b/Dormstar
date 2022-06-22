from re import T
import smbus
import time
import websockets
import asyncio

addr = 0x50
i2c = smbus.SMBus(0)

def get_acc():
    raw_acc_x = i2c.read_i2c_block_data(addr, 0x34, 2)
    raw_acc_y = i2c.read_i2c_block_data(addr, 0x35, 2)
    raw_acc_z = i2c.read_i2c_block_data(addr, 0x36, 2)
    return  raw_acc_x+raw_acc_y+raw_acc_z


def get_angle():
    raw_angle_x = i2c.read_i2c_block_data(addr, 0x3d, 2)
    raw_angle_y = i2c.read_i2c_block_data(addr, 0x3e, 2)
    raw_angle_z = i2c.read_i2c_block_data(addr, 0x3f, 2)
    return raw_angle_x+raw_angle_y+raw_angle_z



async def Trans():
    async with websockets.connect('ws://110.42.138.202:7890') as websocket:
        while True:
            data=bytes(get_acc()+get_angle())
            await websocket.send(data)
            time.sleep(0.1)

asyncio.get_event_loop().run_until_complete(Trans())


