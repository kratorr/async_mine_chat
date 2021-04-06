import asyncio


async def read_chat():
    reader, _ = await asyncio.open_connection('minechat.dvmn.org', 5000)
    while True:
        data = await reader.readline()
        print(data.decode().replace('\n', ''))


asyncio.run(read_chat())