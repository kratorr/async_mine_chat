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

group = parser.add_mutually_exclusive_group()



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

parser.add_argument('-m',
                    '--message',
                    type=str,
                    help='Message text',
                    required=True
                    )

group.add_argument('-n',
                    '--nickname',
                    type=str,
                    help='Nickname for register'
                    )

group.add_argument('-t',
                    '--token',
                     type=str,
                    help='Account hash'
                    )


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
    

async def chat_client(host, port, message, nickname, token):    
    reader, writer = await asyncio.open_connection(host, port)
    if nickname:
        token = await register(host, port, nickname)

    if not token:
        with open('token', 'r') as f:
            token = json.loads(f.readline())['account_hash']
        
    await authorise(writer, reader, token)
    await submit_message(writer, message + '\n')
    
  
if __name__ == '__main__':
    args = parser.parse_args()
    host, port, message, nickname, token = args.host, args.port, args.message, args.nickname, args.token
    asyncio.run(chat_client(host, port, message, nickname, token))