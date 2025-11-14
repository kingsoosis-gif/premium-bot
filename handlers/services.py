from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from utils import usd_to_irr

router = Router()

SERVICES = {
    "موسیقی": {
        "Spotify ۱ ماهه شخصی": 3.99,
        "Spotify ۱ ماهه خانوادگی (۶ نفر)": 6.99,
        "Spotify ۳ ماهه شخصی": 11.97,
        "Spotify ۶ ماهه شخصی": 23.94,
        "Apple Music ۱ ماهه": 5.99,
    },
    "فیلم و سریال": {
        "Netflix ۱ ماهه پروفایل اختصاصی": 6.99,
        "Netflix ۱ ماهه اشتراکی": 2.5,
        "YouTube Premium ۱ ماهه": 4.99,
        "Disney+ ۱ ماهه": 7.99,
    },
    "ابزارها": {
        "ChatGPT Plus ۱ ماهه": 20.0,
        "ChatGPT Plus ۱ ماهه (اشتراکی)": 5.0,
        "Canva Pro ۱ ماهه": 12.99,
        "Midjourney ۱ ماهه": 10.0,
        "Grammarly Premium ۱ ماهه": 12.0,
    },
    "بازی‌ها": {
        "Xbox Game Pass Ultimate ۱ ماهه": 14.99,
        "PlayStation Plus Essential ۱ ماهه": 9.99,
    },
    "سایر خدمات": {
        "Google One ۱۰۰ گیگ": 1.99,
        "NordVPN ۱ ماهه": 11.99,
    }
}

@router.message(lambda m: m.text in SERVICES.keys())
async def show_services(message: types.Message, state: FSMContext):
    cat = message.text
    text = f"دسته: {cat}\n\nلطفاً سرویس مورد نظر رو انتخاب کن:\n\n"
    kb = []
    for name, usd in SERVICES[cat].items():
        irr = usd_to_irr(usd)
        text += f"• {name}\n   💰 {irr}\n\n"
        safe_name = name.replace(" ", "_").replace("(", "").replace(")", "").replace("/", "")
        kb.append([types.InlineKeyboardButton(text=f"خرید {name}", callback_data=f"buy_{safe_name}")])
    kb.append([types.InlineKeyboardButton(text="بازگشت 🔙", callback_data="back_to_categories")])
    
    await message.answer(text, reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb))
    await state.update_data(category=cat)
