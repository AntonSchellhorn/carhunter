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


def listing_keyboard():
    """Кнопки управления под каждым объявлением."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⛔ Стоп",             callback_data="action_stop"),
            InlineKeyboardButton(text="🔄 Обновить сейчас", callback_data="action_refresh"),
            InlineKeyboardButton(text="🔍 Новый поиск",     callback_data="action_new_search"),
        ]
    ])


def language_keyboard():
    """Кнопки выбора языка."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton(text="🇩🇪 Deutsch", callback_data="lang_de"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en"),
        ]
    ])

def sites_keyboard(selected: list):
    """Клавиатура выбора сайтов с чекбоксами."""
    def check(site):
        return "✅" if site in selected else "☑️"

    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"{check('autoscout24')} AutoScout24", callback_data="site_autoscout24"),
            InlineKeyboardButton(text=f"{check('mobile')} Mobile.de",       callback_data="site_mobile"),
        ],
        [
            InlineKeyboardButton(text=f"{check('kleinanzeigen')} Kleinanzeigen", callback_data="site_kleinanzeigen"),
        ],
        [
            InlineKeyboardButton(text="✅ Сохранить", callback_data="sites_save"),
        ]
    ])