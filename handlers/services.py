from aiogram import Router, types
from utils import usd_to_irr

router = Router()

# سرویس‌ها و قیمت دلاری (هر وقت خواستی اضافه یا کم کن)
SERVICES = {
    "موسیقی": {
        "Spotify ۱ ماهه شخصی": 3.99,
        "Spotify ۱ ماهه خانوادگی (۶ نفر)": 6.99,
        "Spotify ۳ ماهه شخصی": 11.97,
        "Spotify ۶ ماهه شخصی": 23.94,
    },
    "فیلم و سریال": {
        "Netflix ۱ ماهه پروفایل اختصاصی": 6.99,
        "Netflix ۱ ماهه اشتراکی": 2.5,
        "YouTube Premium ۱ ماهه": 4.99,
        "Disney+ ۱ ماهه": 7.99,
    },
    "ابزارها": {
        "ChatGPT Plus ۱ ماهه": 20.0,
        "Canva Pro ۱ ماهه": 12.99,
        "Midjourney ۱ ماهه": 10.0,
    }
}

@router.message(lambda m: m.text in SERVICES)
async def show_services(message: types.Message):
    cat = message.text
    text = f"سرویس‌های دسته {cat}:\n\n"
    kb = []
    for name, usd in SERVICES[cat].items():
        irr = usd_to_irr(usd)
        text += f"• {name}\n   قیمت: {irr}\n\n"
        callback = name.replace(" ", "_").replace("(", "").replace(")", "")
        kb.append([types.InlineKeyboardButton(text=f"خرید {name}", callback_data=f"buy_{callback}")])
    kb.append([types.InlineKeyboardButton(text="بازگشت 🔙", callback_data="back_categories")])
    await message.answer(text, reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb))
