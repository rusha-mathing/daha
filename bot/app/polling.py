from aiogram import Dispatcher
from .handlers import router as bot_router
from .bot import bot
from .models import init_db
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
dp = Dispatcher()
dp.include_router(bot_router)

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 