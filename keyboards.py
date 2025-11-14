from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    kb = [
        [KeyboardButton(text="ثبت سفارش"), KeyboardButton(text="قیمت خدمات")],
        [KeyboardButton(text="شارژ حساب"), KeyboardButton(text="اطلاعات حساب")],
        [KeyboardButton(text="پیگیری"), KeyboardButton(text="پشتیبانی")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def back_button():
    return ReplyKeyboardMarkup([[KeyboardButton(text="بازگشت 🔙")]], resize_keyboard=True)
