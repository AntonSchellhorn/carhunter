from aiogram.fsm.state import State, StatesGroup


class SearchForm(StatesGroup):
    make_letter  = State()   # Шаг 1 — Выбор буквы
    make_select  = State()   # Шаг 2 — Выбор марки
    model_select = State()   # Шаг 3 — Выбор модели
    year_from    = State()   # Шаг 4 — Год от
    year_to      = State()   # Шаг 5 — Год до
    price_min    = State()   # Шаг 6 — Минимальная цена
    price_max    = State()   # Шаг 7 — Максимальная цена
    mileage_min  = State()   # Шаг 8 — Минимальный пробег
    mileage_max  = State()   # Шаг 9 — Максимальный пробег
    zip_code     = State()   # Шаг 10 — Почтовый индекс
    radius       = State()   # Шаг 11 — Радиус поиска (км)