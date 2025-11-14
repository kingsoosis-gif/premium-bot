from aiogram import types, Router
from config import CARD_NUMBER, CARD_OWNER

router = Router()

@router.message(lambda message: message.text == "شارژ حساب")
async def wallet_menu(message: types.Message):
    amounts = ["۵۰,۰۰۰", "۱۰۰,۰۰۰", "۲۰۰,۰۰۰", "۵۰۰,۰۰۰", "۱,۰۰۰,۰۰۰", "سایر مبلغ"]
    kb = [[types.KeyboardButton(text=a)] for a in amounts]
    kb.append([types.KeyboardButton(text="بازگشت 🔙")])
    text = f"موجودی فعلی: ۰ تومان\n\nمبلغ مورد نظر رو انتخاب کن:\n\nشماره کارت:\n{CARD_NUMBER}\nبه نام: {CARD_OWNER}"
    await message.answer(text, reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))
