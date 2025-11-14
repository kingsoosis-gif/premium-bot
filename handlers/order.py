from aiogram import Router, types
from aiogram.fsm.context import FSMContext

router = Router()

@router.callback_query(lambda c: c.data.startswith("buy_"))
async def process_buy(callback: types.CallbackQuery, state: FSMContext):
    service_name = callback.data[4:].replace("_", " ")
    data = await state.get_data()
    category = data.get("category", "نامشخص")

    # پیدا کردن قیمت
    price_usd = None
    for services in SERVICES.values():
        if service_name in services:
            price_usd = services[service_name]
            break

    if not price_usd:
        await callback.answer("سرویس پیدا نشد!", show_alert=True)
        return

    from utils import usd_to_irr
    price_irr = usd_to_irr(price_usd)

    text = f"""
سفارش شما ثبت شد ✅

سرویس: {service_name}
دسته: {category}
قیمت نهایی: {price_irr}

لطفاً مبلغ رو به کارت زیر واریز کنید و رسید رو همینجا بفرستید:

شماره کارت:
6037-9997-5312-3456
به نام: سعید درویش

بعد از تأیید پرداخت، اکانت آنی تحویل داده میشه
    """.strip()

    await callback.message.edit_text(text, reply_markup=None)
    await state.update_data(service=service_name, price=price_irr)
    await callback.answer()
