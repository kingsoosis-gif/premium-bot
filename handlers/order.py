from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from utils import usd_to_irr

router = Router()

@router.callback_query(lambda c: c.data.startswith("buy_"))
async def process_buy(callback: types.CallbackQuery, state: FSMContext):
    service_name = callback.data[4:].replace("_", " ")
    data = await state.get_data()
    category = data.get("category", "نامشخص")
    
    # اینجا قیمت رو دوباره پیدا می‌کنیم (برای اطمینان)
    price_usd = None
    for cat, services in {
        "موسیقی": SERVICES["موسیقی"],
        "فیلم و سریال": SERVICES["فیلم و سریال"],
        "ابزارها": SERVICES["ابزارها"],
        "بازی‌ها": SERVICES["بازی‌ها"],
        "سایر خدمات": SERVICES["سایر خدمات"]
    }.items():
        if service_name in services:
            price_usd = services[service_name]
            break
    
    if not price_usd:
        await callback.answer("خطا در پیدا کردن قیمت!", show_alert=True)
        return
    
    price_irr = usd_to_irr(price_usd)
    
    text = f"سفارش شما:\n\nسرویس: {service_name}\nدسته: {category}\nقیمت: {price_irr}\n\nبرای تکمیل خرید، مبلغ رو به کارت زیر واریز کن و رسید رو بفرست:\n\nشماره کارت: 6037-9997-5312-3456\nبه نام: سعید درویش"
    
    await callback.message.edit_text(text, reply_markup=None)
    await state.update_data(service=service_name, price_irr=price_irr.replace(" تومان", "").replace(",", ""))
    await callback.answer()
