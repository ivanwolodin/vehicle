import asyncio
import os
import psutil
import aiohttp.web

try:
    import Combinations # external module. it is working through docker
except ImportError:
    pass


HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))


async def testhandle(request):
    return aiohttp.web.Response(text='Test handle')


async def send_message(message, websocket):
    if message == 'close':
        await websocket.close()
    elif message == 'memory':
        await websocket.send_str('memory statistics: {}'.format(psutil.virtual_memory()))
    elif message == 'cpu':
        await websocket.send_str('cpu load: {}'.format(psutil.cpu_percent()))
    elif message == 'servertime':
        try:
            await websocket.send_str(Combinations.getServerTime())
        except:
            await websocket.send_str('Function implemented, but not properly installed')
    else:
        await websocket.send_str(message + '/function is not implemented')


async def websocket_handler(request):
    print('Websocket connection starting')
    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)
    print('Websocket connection ready')

    async for msg in ws:
        print(msg)
        if msg.type == aiohttp.WSMsgType.TEXT:
            await send_message(message=msg.data,
                               websocket=ws)

    print('Websocket connection closed')
    return ws


def main():
    # loop = asyncio.get_event_loop()
    app = aiohttp.web.Application()
    app.router.add_route('GET', '/', testhandle)
    app.router.add_route('GET', '/ws', websocket_handler)
    aiohttp.web.run_app(app, host=HOST, port=PORT)


if __name__ == '__main__':
    main()
