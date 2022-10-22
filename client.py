import aiohttp
import asyncio

HOST = 'http://127.0.0.1:8080/'


async def main():
    async with aiohttp.ClientSession() as session:

        async with session.get(HOST + 'ads/8') as response:
            print(await response.text())

        async with session.post(HOST + 'ads/',
                                json={'title': 'ГАРАЖ', 'description': 'ГАРАЖ ТОП', 'owner': 'qwerty'}
                                ) as response:
            print(await response.json())

        async with session.put(HOST + 'ads/10',
                               json={'title': 'SALE', 'description': 'SALE'}
                               ) as response:
            print(await response.text())

        async with session.delete(HOST + 'ads/8') as response:
            print(await response.json())


asyncio.run(main())