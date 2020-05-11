from aiohttp import web
import aiohttp
import asyncio

async def hello(request):
    return web.Response(text="Hello, world")


async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    print(ws)
    async for msg in ws:
        print(msg)
        if msg.type == aiohttp.WSMsgType.TEXT:
            print('sdf')
            if msg.data == 'close':
                await ws.close()
            else:
                print('sdf')
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws


# async def websocket_handler(request):
#
#     ws = web.WebSocketResponse()
#     await ws.prepare(request)
#
#     async for msg in ws:
#         if msg.tp == aiohttp.MsgType.text:
#             if msg.data == 'close':
#                 await ws.close()
#             else:
#                 ws.send_str(msg.data)
#         elif msg.tp == aiohttp.MsgType.error:
#             print('ws connection closed with exception %s' %
#                   ws.exception())
#
#     print('websocket connection closed')
#
#     return ws


app = web.Application()
# app.add_routes([web.get('/', hello)])
app.add_routes([web.get('/ws', websocket_handler)])

web.run_app(app)
