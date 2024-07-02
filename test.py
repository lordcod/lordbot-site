import aiohttp
import asyncio

async def main():
    payload = {
        'url': 'https://588f-81-177-135-207.ngrok-free.app/',
        'password': 'aaff2AAfbec0Fbe25CC82cCdE'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:8000/post-api-config/DE05EbFbe596F5ce3E6e707ec', json=payload) as res:
            print(res)

asyncio.run(main())