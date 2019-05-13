import asyncio
import socket
import argparse
from aiofile import AIOFile
from datetime import datetime
import os

DEFAULT_HOST = 'minechat.dvmn.org'
DEFAULT_PORT = 5000
DEFAULT_HISTORY_FILE_PATH = 'history'
DEFAULT_DELAY_BETWEEN_CONNECT_RETRIES = 3


async def retry_connection(host, port, delay):
    try:
        yield await asyncio.open_connection(host, port)
        return
    except (ConnectionRefusedError, socket.gaierror):
        yield 'Нет соединения. Повторная попытка.\n'
    while True:
        try:
            yield await asyncio.open_connection(host, port)
            return
        except (ConnectionRefusedError, socket.gaierror):
            yield f'Нет соединения. Повторная попытка через {delay} сек.\n'
            await asyncio.sleep(delay)


async def read_chat_messages(host, port, delay):
    while True:
        try:
            async for connection_result in retry_connection(host, port, delay):
                if isinstance(connection_result, str):
                    yield connection_result
                    continue
                reader, writer = connection_result
            while True:
                message_data = await reader.readline()
                message_text = message_data.decode()
                datetime_format = '%d.%m.%y %H:%M'
                datetime_string = datetime.now().strftime(datetime_format)
                formatted_message = f'[{datetime_string}] {message_text}'
                yield formatted_message
        except ConnectionResetError:
            yield 'Нет соединения. Повторная попытка.\n'


async def save_messages_to_file(messages_async_generator, filepath):
    async with AIOFile(filepath, 'a') as history_file:
        async for message in messages_async_generator:
            await history_file.write(message)


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host',
                        default=DEFAULT_HOST,
                        help='host name or ip address')
    parser.add_argument('--port',
                        type=int,
                        default=DEFAULT_PORT,
                        help='port')
    parser.add_argument('--history',
                        default=DEFAULT_HISTORY_FILE_PATH,
                        help='path to file with history')
    parser.add_argument('--delay',
                        type=float,
                        default=DEFAULT_DELAY_BETWEEN_CONNECT_RETRIES,
                        help='delay between connect retries')
    args = parser.parse_args()
    host = args.host or os.getenv('HOST') or DEFAULT_HOST
    port = args.port or os.getenv('PORT') or DEFAULT_PORT
    history_file_path = (args.history or os.getenv('HISTORY')
                         or DEFAULT_HISTORY_FILE_PATH)
    delay = (args.delay or os.getenv('DELAY')
             or DEFAULT_DELAY_BETWEEN_CONNECT_RETRIES)
    messages_reader = read_chat_messages(host, port, delay)
    await save_messages_to_file(messages_reader, history_file_path)


if __name__ == '__main__':
    asyncio.run(main())
