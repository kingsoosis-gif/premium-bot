import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import BOT_TOKEN, DEFAULT_PROPERTIES
from database import init_db
from keyboards import main_menu

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, default=DEFAULT_PROPERTIES)
dp = Dispatcher()

# هندلرها رو بعداً ایمپورت می‌کنیم (بعد از ساخت فایل‌هاشون)
from handlers import start, categories, wallet, profile, admin

async def on_startup():
    await init_db()
    print("بات با موفقیت روشن شد! 🚀")

async def main():
    dp.startup.register(on_startup)
    dp.message.register(start.start_handler, Command("start"))
    dp.message.register(start.main_menu_handler)
    # بقیه هندلرها تو فایل‌های خودشون ثبت می‌شن
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
