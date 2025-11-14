from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()

class OrderStates(StatesGroup):
    choosing_category = State()

@router.message(lambda message: message.text == "ثبت سفارش")
async def show_categories(message: types.Message, state: FSMContext):
    kb = [
        [types.KeyboardButton(text="موسیقی")],
        [types.KeyboardButton(text="فیلم و سریال")],
        [types.KeyboardButton(text="بازی‌ها")],
        [types.KeyboardButton(text="اپلیکیشن و ابزارها")],
        [types.KeyboardButton(text="سایر خدمات")],
        [types.KeyboardButton(text="بازگشت 🔙")]
    ]
    await message.answer("دسته‌بندی مورد نظرت رو انتخاب کن:", reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))
    await state.set_state(OrderStates.choosing_category)
