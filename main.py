import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from config import BOT_TOKEN
from database import init_db

# همه روترها (حتماً همه رو اضافه کن)
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

# تنظیمات وب‌هوک
WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = BOT_TOKEN.split(":")[1][:32]  # فقط یه قسمت از توکن برای امنیت
WEBHOOK_URL = f"https://{os.environ['RENDER_EXTERNAL_URL']}{WEBHOOK_PATH}"

async def on_startup(app):
    await init_db()
    await bot.set_webhook(
        url=WEBHOOK_URL,
        secret_token=WEBHOOK_SECRET,
        drop_pending_updates=True
    )
    logging.info(f"Webhook تنظیم شد: {WEBHOOK_URL}")

async def on_shutdown(app):
    logging.info("در حال خاموش شدن...")
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()

async def health(request):
    return web.Response(text="Bot is alive and running on Webhook!")

def main():
    # ثبت همه روترها
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

    # وب‌هوک هندلر
    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET
    ).register(app, path=WEBHOOK_PATH)

    # هلث‌چک برای Render
    app.router.add_get("/", health)

    setup_application(app, dp, bot=bot)
    return app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    web.run_app(main(), host="0.0.0.0", port=port)
