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
# ... بقیه import ها

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# --- تغییرات اینجا شروع می‌شود ---

# به جای استفاده از توکن به عنوان مسیر، یک مسیر ساده انتخاب کنید
WEBHOOK_PATH = "/webhook" 
# از توکن ربات به عنوان توکن امنیتی برای تایید درخواست‌ها استفاده کنید
WEBHOOK_SECRET_TOKEN = BOT_TOKEN 

# --- تغییرات اینجا تمام می‌شود ---


async def on_startup(app):
    logging.info("🚀 تابع on_startup شروع به کار کرد.")
    try:
        await init_db()
        logging.info("✅ دیتابیس با موفقیت راه‌اندازی شد.")

        render_url = os.environ.get("RENDER_EXTERNAL_URL")
        if not render_url:
            logging.critical("❌ CRITICAL: RENDER_EXTERNAL_URL تنظیم نشده است! برنامه متوقف می‌شود.")
            raise RuntimeError("RENDER_EXTERNAL_URL is not set.")

        # آدرس وب‌هوک حالا بسیار ساده و تمیز است
        webhook_url = f"https://{render_url}{WEBHOOK_PATH}"
        
        # تنظیم وب‌هوک با استفاده از secret_token برای امنیت
        await bot.set_webhook(
            url=webhook_url,
            secret_token=WEBHOOK_SECRET_TOKEN
        )
        
        logging.info(f"✅ Webhook با موفقیت تنظیم شد: {webhook_url}")
        logging.info("🎉 بات روی Render با موفقیت فعال شد.")

    except Exception as e:
        logging.critical(f"❌ یک خطای بحرانی در on_startup رخ داد: {e}", exc_info=True)
        raise


async def healthcheck(request):
    return web.Response(text="Bot is running on Render (Webhook Mode)")


def main():
    # ثبت روترها
    dp.include_router(start_router)
    # ... بقیه روترها

    app = web.Application()
    app.on_startup.append(on_startup)

    # ثبت هندلر وب‌هوک با مسیر جدید و توکن امنیتی
    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET_TOKEN  # این پارامتر بسیار مهم است
    ).register(app, path=WEBHOOK_PATH)

    # health check (برای رندر)
    app.router.add_get("/", healthcheck)

    # وصل کردن Aiogram به سرور aiohttp
    setup_application(app, dp, bot=bot)

    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    web.run_app(main(), host="0.0.0.0", port=port)
