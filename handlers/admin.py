from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()

# آیدی خودت (ادمین)
ADMIN_ID = 6990879072  # ← اگه آیدی دیگه‌ای داری عوض کن

class AdminStates(StatesGroup):
    waiting_profit = State()
    waiting_card = State()

# ──────── پنل اصلی ادمین ────────
@router.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    kb = [
        [types.KeyboardButton(text="➕ اضافه کردن سرویس")],
        [types.KeyboardButton(text="✏ ویرایش قیمت/حذف سرویس")],
        [types.Text("💰 تنظیم درصد سود"), types.KeyboardButton(text="💳 تغییر کارت")],
        [types.KeyboardButton(text="👥 لیست کاربران"), types.KeyboardButton(text="📊 آمار فروش")],
        [types.KeyboardButton(text="خروج از پنل ادمین")]
    ]
    await message.answer(
        "به پنل مدیریت خوش اومدی داداش 🔥\n"
        "هر کدوم رو که خواستی بزن:",
        reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    )

# ──────── تنظیم درصد سود ────────
@router.message(lambda m: m.text == "💰 تنظیم درصد سود")
async def set_profit(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer("درصد سود فعلی: {}%\nدرصد جدید رو بفرست (مثلا ۲۸):".format(PROFIT_PERCENT))
    await state.set_state(AdminStates.waiting_profit)

@router.message(AdminStates.waiting_profit)
async def save_profit(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        new = int(message.text)
        # اینجا می‌تونی تو دیتابیس یا config ذخیره کنی (فعلاً فقط متغیر)
        from config import PROFIT_PERCENT
        # برای سادگی فعلاً فقط پیام می‌دیم (بعداً دیتابیس اضافه می‌کنیم)
        await message.answer(f"درصد سود به {new}% تغییر کرد ✅")
        await state.clear()
    except:
        await message.answer("عدد درست بفرست!")

# ──────── بقیه امکانات (به زودی کامل می‌شه) ────────
@router.message(lambda m: m.text and "کارت" in m.text)
async def card_menu(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer(f"کارت فعلی:\n{CARD_NUMBER}\nبه نام {CARD_OWNER}\nشماره کارت جدید بفرست:")

@router.message(lambda m: m.text == "خروج از پنل ادمین")
async def exit_admin(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    from keyboards import main_menu
    await message.answer("از پنل خارج شدی 🔙", reply_markup=main_menu())
