import asyncio
import websockets
def producer_handler(websocket, path):
    print('---- 建立了连接 -----')
    while True:
        message = input('please input:')
        await websocket.send(message)
​
start_server = websockets.serve(producer_handler, 'localhost', 8765)
​
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
