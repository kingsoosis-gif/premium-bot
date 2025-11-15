import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiohttp import web

from config import BOT_TOKEN
from database import init_db

# همه هندلرها
from handlers.start import router as start_router
from handlers.categories import router as categories_router
from handlers.services import router as services_router
from handlers.order import router as order_router
from handlers.wallet import router as wallet_router
from handlers.profile import router as profile_router
from handlers.admin import router as admin_router

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def on_startup():
    await init_db()
    print("بات با موفقیت روشن شد! 🚀")


async def http_healthcheck(request):
    return web.Response(text="Bot is running on Render!")


async def main():
    # ثبت همه روترها
    dp.include_router(start_router)
    dp.include_router(categories_router)
    dp.include_router(services_router)
    dp.include_router(order_router)
    dp.include_router(wallet_router)
    dp.include_router(profile_router)
    dp.include_router(admin_router)

    dp.startup.register(on_startup)

    # اجرای Polling در یک Task جدا
    asyncio.create_task(dp.start_polling(bot))

    # ساخت یک وب‌سرور ساده برای Render
    app = web.Application()
    app.add_routes([web.get("/", http_healthcheck)])

    return app


if __name__ == "__main__":
    # Render پورت 10000 رو دوست داره :)
    web.run_app(main(), port=10000)
