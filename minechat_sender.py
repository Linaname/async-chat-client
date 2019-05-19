import asyncio
import logging
import os
import json
import re
import argparse

TOKEN = '591195a2-75a2-11e9-9d4f-0242ac110002'
DEFAULT_HOST = 'minechat.dvmn.org'
DEFAULT_PORT = 5050
LISTENER_LOGGER = logging.getLogger('listener')
SENDER_LOGGER = logging.getLogger('sender')


async def write_and_log(writer, data, logger=SENDER_LOGGER):
    logger.debug(data.decode())
    writer.write(data)
    await writer.drain()


async def readline_and_log(reader, logger=LISTENER_LOGGER):
    received_data = await reader.readline()
    logger.debug(received_data.decode())
    return received_data


def sanitize_message(message):
    return re.sub(r'(^\n*)|(\n*(?=\n))|(\n*$)', '', message)


def sanitize_nickname(nickname):
    return re.sub(r'\n', '', nickname)


def validate_token(token):
    if '\n' in token:
        raise ValueError('Invalid token')


async def register(host, port, nickname):
    reader, writer = await asyncio.open_connection(host, port)
    greeting = await readline_and_log(reader)
    await write_and_log(writer, b'\n')
    nickname_request_message = await readline_and_log(reader)
    bytes_to_send = nickname.encode() + b'\n'
    await write_and_log(writer, bytes_to_send)
    answer_line_1 = await readline_and_log(reader)
    answer_line_2 = await readline_and_log(reader)
    json_answer = json.loads(answer_line_1.decode())
    token = json_answer['account_hash']
    return reader, writer, token


async def authorize(host, port, token):
    validate_token(token)
    reader, writer = await asyncio.open_connection(host, port)
    greeting = await readline_and_log(reader)
    bytes_to_send = token.encode() + b'\n'
    await write_and_log(writer, bytes_to_send)
    answer_line_1 = await readline_and_log(reader)
    answer_line_2 = await readline_and_log(reader)
    json_answer = json.loads(answer_line_1.decode())
    if json_answer is None:
        raise ValueError('Invalid token')
    return reader, writer


async def send_message(reader, writer, message):
    bytes_to_send = sanitize_message(message).encode() + b'\n\n'
    await write_and_log(writer, bytes_to_send)
    answer = await readline_and_log(reader)


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host',
                        help='host name or ip address')
    parser.add_argument('--port',
                        type=int,
                        help='port')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--token',
                        type=str,
                        help='token')
    group.add_argument('--nickname',
                        type=str,
                        help='nickname')
    parser.add_argument('--message',
                        type=str,
                        help='message text',
                        required=True)
    args = parser.parse_args()
    host = args.host or os.getenv('HOST') or DEFAULT_HOST
    port = args.port or os.getenv('PORT') or DEFAULT_PORT
    token = args.token or os.getenv('TOKEN')
    nickname = args.nickname
    message = args.message or os.getenv('MESSAGE')
    if os.getenv('DEBUG') == '1':
        logging.basicConfig(level=logging.DEBUG)
    if token is not None:
        try:
            reader, writer = await authorize(host, port, token)
        except ConnectionRefusedError:
            exit('Нет соединения')
        except ValueError:
            exit('Неизвестный токен. Проверьте его или зарегистрируйте заново.')
        await send_message(reader, writer, message)
        return
    else:
        try:
            reader, writer, token = await register(host, port, nickname)
        except ConnectionRefusedError:
            exit('Нет соединения')
        print(f'Ваш токен: {token}')
        await send_message(reader, writer, message)
        return


if __name__ == '__main__':
    asyncio.run(main())
