import asyncio
import aiofiles
import argparse
import os
import logging
import json

from datetime import date, datetime

logger = logging.getLogger(__file__)

logging.basicConfig(filename='client.log', level=logging.DEBUG)



parser = argparse.ArgumentParser(description='Async chat client for minechat.')


parser.add_argument('-H',
                    '--host',
                    type=str,
                    default=os.getenv('HOST', default='minechat.dvmn.org'),
                    help='Host address: default=minechat.dvmn.org',
                    )

parser.add_argument('-p',
                    '--port',
                    type=int,
                    default=os.getenv('PORT', default=5050),
                    help='Port; default=5050',
                    )


async def submit_message():
    pass


async def authorise(writer, reader, token):
    message = await reader.readline()
    await submit_message(writer, token)
    message = await reader.readline()

    response = json.loads(message.decode('utf-8'))
    if not response:
        print('Неизвестный токен. Проверьте его или зарегистрируйте заново.')


async def register(host, port, nickname):
    reader, writer = await asyncio.open_connection(host, port)
        
    data = await reader.readline()
    message = data.decode().replace('\n', '')
    logger.debug(message)
    await submit_message(writer, '')
    data = await reader.readline()
    message = data.decode().replace('\n', '')
    logger.debug(message)

    await submit_message(writer, nickname)
    
    data = await reader.readline()
    message = data.decode().replace('\n', '')
    json_message = json.loads(message)
    logger.debug(message)
    with open('token', 'w') as f:
        json.dump(json_message, f)
    writer.close()
    return json_message['account_hash']


async def submit_message(writer, data):
    logger.debug(data)
    data += '\n'
    writer.write(data.encode('utf-8'))
    

async def chat_client(host, port):    
    user_token = input('Введите токен или нажмите Enter для регистрации: ')
    if not user_token:
        nickname = input('Введите ник: ')
        user_token = await register(host, port, nickname)
    
    reader, writer = await asyncio.open_connection(host, port)
    await authorise(writer, reader, user_token)

    while True:
        message = input('Введите сообщение: ')
        await submit_message(writer, message + '\n')
    
  
if __name__ == '__main__':
    args = parser.parse_args()
    host, port = args.host, args.port
    asyncio.run(chat_client(host, port))