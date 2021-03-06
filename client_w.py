import asyncio
try:
    import msvcrt
except ImportError:
    pass
import os
# import sys

import aiohttp

HOST = os.getenv('HOST', '127.0.0.1')
PORT = int(os.getenv('PORT', 8080))

URL = f'http://{HOST}:{PORT}/ws'


async def main():
    session = aiohttp.ClientSession()

    """ контекстный менеджер. 
        Проследит за тем, чтобы сокет корректно закрылся
    """
    async with session.ws_connect(URL) as ws:
        # первая точка остановки. Программа дойдет до сюда и остановится, "зайдя" в функцию prompt_and_send(ws)
        # вернется сюда к тому моменту, когда дойдет до await в функции  prompt_and_send(ws)
        await prompt_and_send(ws)

        # асинхронный цикл, итерируемся, так как после выполнения функции ws.send_str(new_msg_to_send)
        # сервер обязательно отправит ответ
        async for msg in ws:
            print('Message received from server:', msg)
            """ 
            тут снова остановится. Вернёт контекст и продолжит выполнение после того 
            как в функции prompt_and_send(ws) появится результат от await ws.send_str(new_msg_to_send)
            
            """
            await prompt_and_send(ws)  # то есть, остановится на этой строчке

            # если сервер вернул какую-то ошибку в сообщении или закрылся,
            # то сработает break, мы выйдем из цикла
            # и асинхронный менеджер контекста закроет сессию
            if msg.type in (aiohttp.WSMsgType.CLOSED,
                            aiohttp.WSMsgType.ERROR):
                break


async def prompt_and_send(ws):
    # input() блокирующая операция. Тут всё остановится
    new_msg_to_send = input('Type a message to send to the server: ')
    if new_msg_to_send == 'exit':
        print('Exiting!')
        raise SystemExit(0)
    await ws.send_str(new_msg_to_send)


async def prompt_and_send_v2(ws, raw_data):
    message, timeout = prepare_data(raw_data)
    # message = raw_data
    if message == 'exit':
        print('Exiting!')
        raise SystemExit(0)
    await asyncio.sleep(timeout)
    await ws.send_str(message)


def prepare_data(raw_input):
    if len(raw_input.split('-')) == 2:
        message, timeout = raw_input.split('-')
    elif len(raw_input.split('_')) == 2:
        message, timeout = raw_input.split('_')
    else:
        message = raw_input
        timeout = 3
    # print(message, int(timeout))
    return message, int(timeout)


async def main_v2():
    session = aiohttp.ClientSession()

    async with session.ws_connect(URL) as ws:
        new_msg_to_send = input('Type a message to send to the server: ')

        await prompt_and_send_v2(ws=ws,
                                 raw_data=new_msg_to_send)
        async for msg in ws:
            print('Message received from server:', msg)
            try:
                if msvcrt.kbhit():
                    new_msg_to_send = input('Type a message to send to the server: ')
                    await prompt_and_send_v2(ws=ws,
                                             raw_data=new_msg_to_send)
            except:
                await prompt_and_send_v2(ws=ws,
                                     raw_data=new_msg_to_send)

            if msg.type in (aiohttp.WSMsgType.CLOSED,
                            aiohttp.WSMsgType.ERROR):
                break


if __name__ == '__main__':
    print('Type "exit" to quit')      # просто информационное сообщение

    """создаем эвент-луп, то есть создаем ситуацию, когда 
       одна подпрограмма, дойдя до какого-то момента (точнее, до конструкции await prompt_and_send(),
       вернёт контекст (то есть вернет управление, начнет выполнять другую подпрограмму и будет ждать, 
       пока снова не дойдет до конструкции await some_function().
       После этого вернется к предыдущему await prompt_and_send() и продолжит выполнение 
       до следующего await
    
    """
    loop = asyncio.get_event_loop()

    """Здесь запускаем всю капусту"""
    # loop.run_until_complete(main())
    loop.run_until_complete(main_v2())
