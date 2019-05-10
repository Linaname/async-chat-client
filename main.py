import asyncio
import socket

HOST = 'minechat.dvmn.org'
PORT = 5000


async def retry_connection(host, port, delay):
    try:
        return await asyncio.open_connection(host, port)
    except (ConnectionRefusedError, socket.gaierror):
        print('Нет соединения. Повторная попытка.')
    while True:
        try:
            return await asyncio.open_connection(host, port)
        except (ConnectionRefusedError, socket.gaierror):
            print(f'Нет соединения. Повторная попытка через {delay} сек.')
            await asyncio.sleep(delay)


async def display_chat_messages(host, port, delay=3):
    while True:
        try:
            reader, writer = await retry_connection(host, port, delay)
            while True:
                message = await reader.readline()
                print(message.decode())
        except ConnectionResetError:
            print('Нет соединения. Повторная попытка.')

asyncio.run(display_chat_messages(HOST, PORT))
