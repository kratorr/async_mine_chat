import asyncio
import aiofiles
import argparse
import os
import logging
import json

from datetime import date, datetime

from asyncio.tasks import sleep


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


async def send_data(writer, data):
    logger.debug(data)
    data += '\n'
    writer.write(data.encode('utf-8'))
    

async def chat_client(host, port):
    reader, writer = await asyncio.open_connection(host, port)
        
   # while True:
    data = await reader.readline()
    message = data.decode().replace('\n', '')
    logger.debug(message)
    
    #await send_data(writer, '4206afde-9c2c-11eb-8c47-0242ac110002\n'.encode('utf-8'))
    
    user_token = input('Введите токен: ')
    await send_data(writer, user_token)
    
    message = await reader.readline()
    
    response = json.loads(message.decode('utf-8'))
    if not response:
        print('Неизвестный токен. Проверьте его или зарегистрируйте заново.')
    await send_data(writer, 'test message\n')

    writer.close()
        

if __name__ == '__main__':
    args = parser.parse_args()
    host, port = args.host, args.port
    asyncio.run(chat_client(host, port))