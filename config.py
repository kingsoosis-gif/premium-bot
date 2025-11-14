import os
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

BOT_TOKEN = os.getenv("BOT_TOKEN", "8364048690:AAH9_IlFR25KS5NhNbnjX_vzNd_PJ4zHCks")
DEFAULT_PROPERTIES = DefaultBotProperties(parse_mode=ParseMode.HTML)

# تنظیمات اولیه (از پنل ادمین تغییر می‌کنی)
PROFIT_PERCENT = 28
CARD_NUMBER = "6037999753123456"
CARD_OWNER = "سعید درویش"
WELCOME_MESSAGE = "به فروشگاه اشتراک پرمیوم خوش اومدی 🎧✨"
