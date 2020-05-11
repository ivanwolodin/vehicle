import asyncio
import os
import psutil
import aiohttp.web

import Combinations # external module. it is working through docker

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))


async def testhandle(request):
    return aiohttp.web.Response(text='Test handle')


async def websocket_handler(request):
    print('Websocket connection starting')
    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)
    print('Websocket connection ready')

    async for msg in ws:
        print(msg)
        if msg.type == aiohttp.WSMsgType.TEXT:
            print(msg.data)
            if msg.data == 'close':
                await ws.close()
            elif msg.data == 'memory':
                await ws.send_str('memory statistics: {}'.format(psutil.virtual_memory()))
            elif msg.data == 'servertime':
                await ws.send_str(Combinations.getServerTime())
            elif msg.data == 'cpu':
                await ws.send_str('cpu load: {}'.format(psutil.cpu_percent()))
            else:
                await ws.send_str(msg.data + '/function is not implemented')

    print('Websocket connection closed')
    return ws


def main():
    loop = asyncio.get_event_loop()
    app = aiohttp.web.Application(loop=loop)
    app.router.add_route('GET', '/', testhandle)
    app.router.add_route('GET', '/ws', websocket_handler)
    aiohttp.web.run_app(app, host=HOST, port=PORT)


if __name__ == '__main__':
    main()
