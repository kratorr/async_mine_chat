import asyncio
import aiofiles
import argparse
import os

from datetime import date, datetime



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
                    help='Port; default=5000',
                    )


async def chat_client(host, port):
    reader, writer = await asyncio.open_connection(host, port)
        
    while True:
        data = await reader.readline()
        message = data.decode().replace('\n', '')
        now = datetime.now().strftime("%d.%m.%y %H:%m")
        print(message)
        writer.write('4206afde-9c2c-11eb-8c47-0242ac110002\n'.encode('utf-8'))
        writer.write('test message\n\n'.encode('utf-8'))
        break
    writer.close()
        

if __name__ == '__main__':
    args = parser.parse_args()
    host, port = args.host, args.port
    asyncio.run(chat_client(host, port))