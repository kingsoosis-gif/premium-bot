from aiogram import types, Router

router = Router()

@router.message(lambda message: message.text == "اطلاعات حساب")
async def show_profile(message: types.Message):
    text = ("پروفایل شما\n\n"
            "آیدی: @{username}\n"
            "آیدی عددی: {id}\n"
            "موجودی: ۰ تومان\n"
            "تعداد سفارش: ۰\n"
            "مجموع خرید: ۰ تومان\n"
            "سطح: عادی").format(username=message.from_user.username or "ندارد", id=message.from_user.id)
    await message.answer(text, reply_markup=types.ReplyKeyboardMarkup([[types.KeyboardButton(text="بازگشت 🔙")]], resize_keyboard=True))
