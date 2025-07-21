import logging

from aiogram import Router, types, F
from aiogram.filters import Command, CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .daha_api import fetch_endpoint, link_telegram_account
from .models import invert_subject, invert_difficulty, get_subjects_by_telegram_id, get_difficulties_by_telegram_id

router = Router()

async def build_choice_keyboard(choose_type, user_id):
    data = await fetch_endpoint(choose_type)
    if not isinstance(data, list):
        data = [data] if data is not None else []

    # Приводим к списку пар (label, value)
    items = []
    seen_values = set()
    for item in data:
        if isinstance(item, dict):
            value = str(item.get("type", "")).strip()[:60]
            label = str(item.get("label", value)).strip()
        else:
            value = str(item).strip()[:60]
            label = str(item).strip()
        if not value:
            continue
        value = ''.join(c for c in value if c.isalnum() or c in "_-")
        if not value or value in seen_values:
            continue
        seen_values.add(value)
        items.append((label, value))
        print(f"Button: label={label!r}, value={value!r}")

    if choose_type == "subjects":
        chosen_types = await get_subjects_by_telegram_id(user_id)
    elif choose_type == "difficulties":
        chosen_types = await get_difficulties_by_telegram_id(user_id)
    else:
        chosen_types = []
    if not isinstance(chosen_types, list):
        chosen_types = [chosen_types] if chosen_types is not None else []
    elif chosen_types and isinstance(chosen_types[0], dict):
        chosen_types = [str(x.get("type", str(x))).strip() for x in chosen_types]

    builder = InlineKeyboardBuilder()
    for label, value in items:
        checked = " ✅" if value in chosen_types else ""
        builder.button(text=f"{label}{checked}", callback_data=f"{choose_type}_{value}")

    builder.button(text="Назад ↩", callback_data="start")
    builder.adjust(1)
    return builder.as_markup()

@router.message(Command("link"))
async def handle_link_command(message: types.Message, command: CommandObject):
    """Handles the /link command to connect a Telegram account with a web account."""
    token = command.args
    if not token:
        await message.answer("Пожалуйста, укажите код для привязки. Пример: /link <ваш_код>")
        return

    telegram_id = message.from_user.id
    result = await link_telegram_account(token, telegram_id)

    if result.get("success"):
        username = result["data"].get("username", "ваш аккаунт")
        await message.answer(f"✅ Ваш Telegram-аккаунт успешно привязан к профилю {username}!")
    else:
        error_message = result.get("error", "Произошла неизвестная ошибка.")
        await message.answer(f"❌ Не удалось привязать аккаунт. Ошибка: {error_message}")

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
    await callback.message.edit_text("Выбирай:", reply_markup=markup)
    await callback.answer()


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
    builder = InlineKeyboardBuilder()
    builder.button(text="Выбрать предметы", callback_data="choose_subjects")
    builder.button(text="Выбрать уровни сложности", callback_data="choose_difficulties")

    await callback.message.edit_text("Привет! Задай предметы и сложности, которые тебя интересуют, чтобы получать уведомления о соответствующих новых курсах!",
                         reply_markup=builder.as_markup())
    await callback.answer()