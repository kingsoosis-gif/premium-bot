from aiogram import types, Router
from keyboards import main_menu

router = Router()

@router.message(lambda message: message.text == "شروع مجدد" or "/start")
async def start_handler(message: types.Message):
    welcome = "به فروشگاه اشتراک‌های پرمیوم خوش اومدی 🎧✨\n\nاینجا می‌تونی اشتراک رسمی اسپاتیفای، نتفلیکس، چت‌جی‌پی‌تی و ده‌ها سرویس دیگه رو با بهترین قیمت و تحویل آنی بگیری!\n\nلطفاً یکی از گزینه‌های زیر رو انتخاب کن:"
    await message.answer(welcome, reply_markup=main_menu())
