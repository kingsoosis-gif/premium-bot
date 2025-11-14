import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import BOT_TOKEN, ADMIN_IDS, WELCOME_TEXT
from database import init_db

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        f"سلام {message.from_user.first_name}!\n\n"
        f"{WELCOME_TEXT}\n\n"
        "بات در حال راه‌اندازیه... خیلی زود منوی کامل باز می‌شه ❤️\n\n"
        "اگر ادمین هستی /admin بزن"
    )

@dp.message(Command("admin"))
async def admin_cmd(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        ADMIN_IDS.append(message.from_user.id)
        await message.answer("ادمین گرامی خوش اومدی! ✅\nپنل کامل به زودی اضافه می‌شه")
    else:
        await message.answer("به پنل مدیریت خوش اومدی 🔥")

async def main():
    await init_db()
    print("بات داره روشن می‌شه...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
