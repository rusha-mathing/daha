import asyncio

from contextlib import asynccontextmanager
from fastapi import FastAPI
from aiogram import Dispatcher
from handlers import router as bot_router
from webhook import router as webhook_router
from bot import bot


dp = Dispatcher()
dp.include_router(bot_router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(dp.start_polling(bot))
    yield
    task.cancel()

app = FastAPI(lifespan=lifespan)
app.include_router(webhook_router, prefix="/webhook")

