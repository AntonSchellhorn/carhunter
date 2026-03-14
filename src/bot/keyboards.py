from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def confirm_keyboard():
    """Кнопки в конце диалога — Запустить или Начать заново."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Запустить поиск", callback_data="confirm_search"),
            InlineKeyboardButton(text="🔄 Начать заново",  callback_data="restart_search"),
        ]
    ])


def skip_keyboard():
    """Кнопка Пропустить — для необязательных полей."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="⏭ Пропустить")]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )