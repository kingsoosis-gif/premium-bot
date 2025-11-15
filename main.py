import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

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

WEBHOOK_SECRET = BOT_TOKEN   # برای امنیت، آدرس وبهوک = توکن


async def on_startup(app):
    await init_db()
    render_url = os.environ.get("RENDER_EXTERNAL_URL")
    if not render_url:
        print("⚠ RENDER_EXTERNAL_URL تنظیم نشده!")
        return

    webhook_url = f"https://{render_url}/{WEBHOOK_SECRET}"
    await bot.set_webhook(webhook_url)

    print("Webhook set:", webhook_url)
    print("بات روی Render فعال شد ✔")


async def healthcheck(request):
    return web.Response(text="Bot is running on Render (Webhook Mode)")


def main():
    # ثبت روترها
    dp.include_router(start_router)
    dp.include_router(categories_router)
    dp.include_router(services_router)
    dp.include_router(order_router)
    dp.include_router(wallet_router)
    dp.include_router(profile_router)
    dp.include_router(admin_router)

    app = web.Application()

    # مسیر وبهوک
    SimpleRequestHandler(dp, bot).register(app, path=f"/{WEBHOOK_SECRET}")

    # health check (برای رندر)
    app.router.add_get("/", healthcheck)

    # وصل کردن Aiogram به سرور aiohttp
    setup_application(app, dp, bot=bot)

    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    web.run_app(main(), host="0.0.0.0", port=port)
