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
    body_type    = State()   # Шаг 10 — Тип кузова
    fuel_type    = State()   # Шаг 11 — Тип топлива
    transmission = State()   # Шаг 12 — Коробка передач
    condition    = State()   # Шаг 13 — Состояние
    seller_type  = State()   # Шаг 14 — Частник или дилер
    damage       = State()   # Шаг 15 — Аварийность
    zip_code     = State()   # Шаг 16 — Почтовый индекс
    radius       = State()   # Шаг 17 — Радиус поиска