import asyncio
import aiofiles
import argparse
import os

from datetime import  datetime



parser = argparse.ArgumentParser(description='Async reader chat for minechat.')


parser.add_argument('-H',
                    '--host',
                    type=str,
                    default=os.getenv('HOST', default='minechat.dvmn.org'),
                    help='Host address: default=minechat.dvmn.org',
                    )

parser.add_argument('-p',
                    '--port',
                    type=int,
                    default=os.getenv('PORT', default=5000),
                    help='Port; default=5000',
                    )

parser.add_argument('--history',
                    type=str,
                    default=os.getenv('LOG', default='./chat.log'),
                    help='Chat log file path; default=./chat.log',
                    )


async def read_chat(host, port, history_path):
    reader, _ = await asyncio.open_connection(host, port)
    async with aiofiles.open(history_path, mode='a') as file:
        
        while True:
            data = await reader.readline()
            message = data.decode().replace('\n', '')
            now = datetime.now().strftime("%d.%m.%y %H:%m")
            print(message)
            await file.writelines(f"[{now}] {message}\n")
            await file.flush()
   

if __name__ == '__main__':
    args = parser.parse_args()
    host, port, history_path = args.host, args.port, args.history
    asyncio.run(read_chat(host, port, history_path))