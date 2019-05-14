import asyncio
import socket
import argparse
from aiofile import AIOFile
from datetime import datetime, timedelta
import os
import config


async def async_messages_generator(host, port, delay, tries_without_delay=2):
    failed_tries_count = 0
    while True:
        while True:
            try:
                reader, writer = await asyncio.open_connection(host, port)
                failed_tries_count = 0
                break
            except (ConnectionRefusedError, socket.gaierror):
                failed_tries_count += 1
                if failed_tries_count < tries_without_delay:
                    yield 'Нет соединения. Повторная попытка.\n'
                else:
                    yield (f'Нет соединения.'
                           f' Повторная попытка через {delay} сек.\n')
                    await asyncio.sleep(delay)
        while True:
            try:
                message_data = await reader.readline()
            except ConnectionResetError:
                yield 'Нет соединения. Повторная попытка.\n'
                break
            message_text = message_data.decode()
            datetime_format = '%d.%m.%y %H:%M'
            datetime_string = datetime.now().strftime(datetime_format)
            formatted_message = f'[{datetime_string}] {message_text}'
            yield formatted_message


async def save_messages_to_file(messages_generator, filepath):
    async with AIOFile(filepath, 'a') as history_file:
        async for message in messages_generator:
            await history_file.write(message)


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host',
                        help='host name or ip address')
    parser.add_argument('--port',
                        type=int,
                        help='port')
    parser.add_argument('--history',
                        help='path to file with history')
    parser.add_argument('--delay',
                        type=float,
                        help='delay between connect retries')
    args = parser.parse_args()
    host = args.host or os.getenv('HOST') or config.DEFAULT_HOST
    port = args.port or os.getenv('PORT') or config.DEFAULT_LISTENER_PORT
    history_file_path = (args.history or os.getenv('HISTORY')
                         or config.DEFAULT_HISTORY_FILE_PATH)
    delay = (args.delay or os.getenv('DELAY')
             or config.DEFAULT_DELAY_BETWEEN_CONNECT_RETRIES)
    messages_generator = async_messages_generator(host, port, delay)
    await save_messages_to_file(messages_generator, history_file_path)


if __name__ == '__main__':
    asyncio.run(main())
