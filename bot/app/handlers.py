from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from daha_api import fetch_endpoint
from models import invert_subject, invert_difficulty, get_subjects_by_telegram_id, get_difficulties_by_telegram_id

router = Router()

async def build_choice_keyboard(choose_type, user_id):
    data = await fetch_endpoint(choose_type)

    if choose_type == "subjects":
        chosen_types = await get_subjects_by_telegram_id(user_id)
    elif choose_type == "difficulties":
        chosen_types = await get_difficulties_by_telegram_id(user_id)
    else:
        chosen_types = []
    builder = InlineKeyboardBuilder()
    for item in data:
        checked = " ✅" if item["type"] in chosen_types else ""
        builder.button(text=f"{item['label']}{checked}", callback_data=f"{choose_type}_{item['type']}")

    builder.button(text="Назад ↩", callback_data="start")
    builder.adjust(1)
    return builder.as_markup()

@router.message(Command("start"))
async def handle_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="Выбрать предметы", callback_data="choose_subjects")
    builder.button(text="Выбрать уровни сложности", callback_data="choose_difficulties")

    await message.answer("Привет! Задай предметы и сложности, которые тебя интересуют, чтобы получать уведомления о соответствующих новых курсах!",
                         reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("choose_"))
async def handle_type_choice(callback: types.CallbackQuery):
    choose_type = callback.data.removeprefix("choose_")
    markup = await build_choice_keyboard(choose_type, callback.from_user.id)
    await callback.message.answer("Выбирай:", reply_markup=markup)


@router.callback_query(F.data.startswith("subjects_"))
async def handle_subject_choice(callback: types.CallbackQuery):
    subject_type = callback.data.removeprefix("subjects_")
    await invert_subject(callback.from_user.id, subject_type)
    markup = await build_choice_keyboard("subjects", callback.from_user.id)
    await callback.message.edit_reply_markup(reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data.startswith("difficulties_"))
async def handle_difficulty_choice(callback: types.CallbackQuery):
    difficulty_type = callback.data.removeprefix("difficulties_")
    await invert_difficulty(callback.from_user.id, difficulty_type)
    markup = await build_choice_keyboard("difficulties", callback.from_user.id)
    await callback.message.edit_reply_markup(reply_markup=markup)
    await callback.answer()

@router.callback_query(F.data == "start")
async def handle_back_to_start(callback: types.CallbackQuery):
    await callback.message.delete()