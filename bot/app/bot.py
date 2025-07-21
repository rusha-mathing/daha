from aiogram import Bot
from .config import BotSettings

settings = BotSettings()
bot = Bot(token=settings.BOT_TOKEN)
