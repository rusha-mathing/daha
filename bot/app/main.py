import asyncio

from fastapi import FastAPI
from .webhook import router as webhook_router
from .api import router as api_router

app = FastAPI()
app.include_router(webhook_router, prefix="/webhook")
app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    from aiogram import Dispatcher
    from .handlers import router as bot_router
    from .bot import bot
    from .config import settings
    import uvicorn

    dp = Dispatcher()
    dp.include_router(bot_router)

    async def start_polling():
        await dp.start_polling(bot)

    loop = asyncio.get_event_loop()
    loop.create_task(start_polling())
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)

