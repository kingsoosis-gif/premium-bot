from aiogram import types, Router

router = Router()
ADMIN_ID = 6990879072  # آیدی خودت

@router.message(lambda message: message.text == "/admin" and message.from_user.id == ADMIN_ID)
async def admin_panel(message: types.Message):
    kb = [
        [types.KeyboardButton(text="مدیریت سرویس‌ها")],
        [types.KeyboardButton(text="مدیریت کاربران")],
        [types.KeyboardButton(text="تنظیمات کارت و سود")],
        [types.KeyboardButton(text="خروج از پنل")]
    ]
    await message.answer("به پنل مدیریت خوش اومدی 🔥", reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))
