import websockets
import asyncio

async def hello(websocket,path):
    while True:
         data = await websocket.recv()
         print(data)
                

start_server = websockets.serve(hello,'0.0.0.0',7890)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
