import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# توکن رو از Environment می‌گیره
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

# این دو خط جدید مهم هستن
default_properties = DefaultBotProperties(parse_mode=ParseMode.HTML)
bot = Bot(token=BOT_TOKEN, default=default_properties)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "سلام داداش! بات با موفقیت روشن شد! ❤️\n\n"
        "الان همه چیز آماده‌ست، فقط منتظر نسخه کامل و خفن باشیم 🔥\n\n"
        "ادمین: /admin"
    )

@dp.message(Command("admin"))
async def admin_cmd(message: types.Message):
    await message.answer("ادمین گرامی خوش اومدی! پنل کامل خیلی زود میاد 🚀")

async def main():
    print("بات داره روشن می‌شه...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
