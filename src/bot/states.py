from aiogram.fsm.state import State, StatesGroup


class SearchForm(StatesGroup):
    make        = State()   # Шаг 1 — Марка
    model       = State()   # Шаг 2 — Модель
    year_from   = State()   # Шаг 3 — Год от
    year_to     = State()   # Шаг 4 — Год до
    price_max   = State()   # Шаг 5 — Максимальная цена
    mileage_max = State()   # Шаг 6 — Максимальный пробег