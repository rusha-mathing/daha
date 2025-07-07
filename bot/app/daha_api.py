import asyncio

import aiohttp
import os

from dotenv import load_dotenv

load_dotenv()
URL = os.getenv("API_URL")

async def fetch_endpoint(endpoint):
    async with aiohttp.ClientSession() as session:
        resp = await session.get(URL + endpoint)
        data = await resp.json()
        print(data)
        return data
