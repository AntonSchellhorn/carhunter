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
        ],
        [
            InlineKeyboardButton(text="⚙️ Меню настроек",  callback_data="action_menu"),
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

def interval_keyboard(selected: int):
    """Клавиатура выбора интервала проверки."""
    def check(minutes):
        return "✅" if selected == minutes else ""

    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"{check(5)} 5 мин",   callback_data="interval_5"),
            InlineKeyboardButton(text=f"{check(15)} 15 мин", callback_data="interval_15"),
            InlineKeyboardButton(text=f"{check(30)} 30 мин", callback_data="interval_30"),
        ],
        [
            InlineKeyboardButton(text=f"{check(60)} 1 час",   callback_data="interval_60"),
            InlineKeyboardButton(text=f"{check(180)} 3 часа", callback_data="interval_180"),
            InlineKeyboardButton(text=f"{check(360)} 6 часов",callback_data="interval_360"),
        ],
        [
            InlineKeyboardButton(text=f"{check(720)} 12 часов", callback_data="interval_720"),
            InlineKeyboardButton(text=f"{check(1440)} 24 часа", callback_data="interval_1440"),
        ],
    ])

def make_letter_keyboard():
    """Клавиатура выбора первой буквы марки."""
    from makes import MAKES
    
    # Собираем уникальные первые буквы
    letters = sorted(set(make[0].upper() for make in MAKES.keys()))
    
    # Разбиваем на ряды по 5 кнопок
    rows = []
    row = []
    for i, letter in enumerate(letters):
        row.append(InlineKeyboardButton(text=letter, callback_data=f"letter_{letter}"))
        if len(row) == 5:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    
    return InlineKeyboardMarkup(inline_keyboard=rows)


def make_select_keyboard(letter: str):
    """Клавиатура выбора марки по букве."""
    from makes import MAKES
    
    makes = [make for make in MAKES.keys() if make[0].upper() == letter]
    
    rows = []
    for make in sorted(makes):
        rows.append([InlineKeyboardButton(text=make, callback_data=f"make_{make[:30]}")])
    
    rows.append([InlineKeyboardButton(text="◀️ Назад", callback_data="make_back")])
    
    return InlineKeyboardMarkup(inline_keyboard=rows)


def model_select_keyboard(make: str):
    """Клавиатура выбора модели."""
    from makes import MAKES
    
    models = MAKES.get(make, [])
    
    rows = []
    # Кнопка "Все модели" всегда первая
    rows.append([InlineKeyboardButton(text="📋 Все модели", callback_data="model_all")])
    
    for model in models:
        rows.append([InlineKeyboardButton(text=model, callback_data=f"model_{model[:30]}")])
    
    rows.append([InlineKeyboardButton(text="◀️ Назад", callback_data="model_back")])
    
    return InlineKeyboardMarkup(inline_keyboard=rows)


def settings_keyboard():
    """Меню настроек."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🌍 Язык",             callback_data="menu_language"),
            InlineKeyboardButton(text="🌐 Сайты",            callback_data="menu_sites"),
        ],
        [
            InlineKeyboardButton(text="⏱ Интервал",         callback_data="menu_interval"),
            InlineKeyboardButton(text="📊 Статус",           callback_data="menu_status"),
        ],
        [
            InlineKeyboardButton(text="🔍 Новый поиск",      callback_data="action_new_search"),
            InlineKeyboardButton(text="⛔ Стоп",             callback_data="action_stop"),
        ],
        [
            InlineKeyboardButton(text="❌ Закрыть",          callback_data="menu_close"),
        ]
    ])


def radius_keyboard():
    """Клавиатура выбора радиуса поиска."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="10 км",  callback_data="radius_10"),
            InlineKeyboardButton(text="25 км",  callback_data="radius_25"),
            InlineKeyboardButton(text="50 км",  callback_data="radius_50"),
        ],
        [
            InlineKeyboardButton(text="100 км", callback_data="radius_100"),
            InlineKeyboardButton(text="200 км", callback_data="radius_200"),
            InlineKeyboardButton(text="🌍 Вся Германия", callback_data="radius_0"),
        ],
    ])