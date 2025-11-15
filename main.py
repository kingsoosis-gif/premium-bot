import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from config import BOT_TOKEN
from database import init_db

# همه روترها
from handlers.start import router as start_router
from handlers.categories import router as categories_router
from handlers.services import router as services_router
from handlers.order import router as order_router
from handlers.wallet import router as wallet_router
from handlers.profile import router as profile_router
from handlers.admin import router as admin_router

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = "my_super_secret_token_2025"  # یه متن ثابت، هر چی دوست داری

async def on_startup(app):
    await init_db()
    
    # این متغیر رو Render خودش اتوماتیک ست می‌کنه
    render_url = os.getenv("RENDER_EXTERNAL_URL")
    if not render_url:
        logging.error("RENDER_EXTERNAL_URL پیدا نشد! ۳۰ ثانیه صبر می‌کنیم...")
        await asyncio.sleep(30)
        render_url = os.getenv("RENDER_EXTERNAL_URL")
    
    if not render_url:
        logging.critical("هنوز URL نداریم، از polling استفاده می‌کنیم (موقتاً)")
        return

    webhook_url = f"https://{render_url}{WEBHOOK_PATH}"
    
    try:
        await bot.set_webhook(
            url=webhook_url,
            secret_token=WEBHOOK_SECRET,
            drop_pending_updates=True
        )
        logging.info(f"وب‌هوک با موفقیت تنظیم شد: {webhook_url}")
    except Exception as e:
        logging.error(f"خطا در تنظیم وب‌هوک: {e}")

async def on_shutdown(app):
    logging.info("در حال حذف وب‌هوک...")
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()

async def health(request):
    return web.Response(text="Bot is alive! Webhook Mode Active")

def main():
    dp.include_router(start_router)
    dp.include_router(categories_router)
    dp.include_router(services_router)
    dp.include_router(order_router)
    dp.include_router(wallet_router)
    dp.include_router(profile_router)
    dp.include_router(admin_router)

    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET
    ).register(app, path=WEBHOOK_PATH)

    app.router.add_get("/", health)
    setup_application(app, dp, bot=bot)
    return app

if __name__ == "__main__":
    import asyncio
    port = int(os.environ.get("PORT", 10000))
    web.run_app(main(), host="0.0.0.0", port=port)
