import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from database import init_db
from keyboards import main_menu

# فقط این هندلرها الان وجود دارن
from handlers.start import router as start_router
from handlers.categories import router as categories_router
from handlers.wallet import router as wallet_router
from handlers.profile import router as profile_router
from handlers.admin import router as admin_router

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

async def on_startup():
    await init_db()
    print("بات با موفقیت روشن شد! 🚀")

async def main():
    # ثبت فقط هندلرهای موجود
    dp.include_router(start_router)
    dp.include_router(categories_router)
    dp.include_router(wallet_router)
    dp.include_router(profile_router)
    dp.include_router(admin_router)

    dp.startup.register(on_startup)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
