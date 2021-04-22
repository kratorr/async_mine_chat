import asyncio
import logging
import os
import argparse
import json

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
    logger.debug(f'Send: {data}')
    data += '\n'
    writer.write(data.encode('utf-8'))


async def chat_client(host, port):
    reader, writer = await asyncio.open_connection(host, port)
        
    data = await reader.readline()
    message = data.decode().replace('\n', '')
    
    logger.debug(message)

    await send_data(writer, '')
    data = await reader.readline()
    message = data.decode().replace('\n', '')
    
    logger.debug(message)

    nick = input('Enter your nick: ')

    await send_data(writer, nick)
    
    data = await reader.readline()
    message = data.decode().replace('\n', '')
    json_message = json.loads(message)
    logger.debug(message)
    with open('token', 'w') as f:
        json.dump(json_message, f)
    

    writer.close()
        

if __name__ == '__main__':
    args = parser.parse_args()
    host, port = args.host, args.port
    asyncio.run(chat_client(host, port))