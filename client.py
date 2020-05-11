import aiohttp
import asyncio


async def socket_client_request():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(url='http://127.0.0.1:8080/ws') as ws:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    if msg.data == 'close cmd':
                        await ws.close()
                        break
                    else:
                        await ws.send_str(msg.data + '/answer')
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    print('Mut')
                    break


async def http_client_request():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:5001/') as resp:
            print(resp.status)
            print(await resp.text())





loop = asyncio.get_event_loop()
# loop.run_until_complete(http_client_request())
loop.run_until_complete(socket_client_request())



