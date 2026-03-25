from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from scheduler import check_new_listings
from keyboards import (
confirm_keyboard, skip_keyboard,
listing_keyboard, language_keyboard, sites_keyboard,
interval_keyboard, make_letter_keyboard, make_select_keyboard,
model_select_keyboard, settings_keyboard, radius_keyboard
)
from database import (
save_search, get_search, set_active, 
set_language, get_language, get_sites, set_sites,
get_interval, set_interval,get_zip, set_zip
)
from locales import t
from states import SearchForm

router = Router()


# ─────────────────────────────────────────
#  /start
# ─────────────────────────────────────────
@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "🌍 Выбери язык / Sprache wählen / Choose language:",
        reply_markup=language_keyboard(),
    )

# ─────────────────────────────────────────
#  Выбор языка
# ─────────────────────────────────────────
@router.callback_query(F.data.in_({"lang_ru", "lang_de", "lang_en"}))
async def choose_language(callback: CallbackQuery):
    lang = callback.data.split("_")[1]  # "lang_ru" → "ru"
    await set_language(callback.from_user.id, lang)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        t(lang, "welcome"),
        parse_mode="HTML",
    )
    await callback.answer()


# ─────────────────────────────────────────
#  /search — запуск диалога
# ─────────────────────────────────────────
@router.message(Command("search"))
async def cmd_search(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🔍 Шаг 1 — Выбери первую букву марки:",
        reply_markup=make_letter_keyboard(),
    )
    await state.set_state(SearchForm.make_letter)


@router.callback_query(F.data.startswith("letter_"), SearchForm.make_letter)
async def choose_letter(callback: CallbackQuery, state: FSMContext):
    letter = callback.data.replace("letter_", "")  # "letter_B" → "B"
    await state.update_data(letter=letter)
    await callback.message.edit_text(
        f"🔍 Шаг 2 — Выбери марку на букву <b>{letter}</b>:",
        parse_mode="HTML",
        reply_markup=make_select_keyboard(letter),
    )
    await state.set_state(SearchForm.make_select)
    await callback.answer()


@router.callback_query(F.data == "make_back", SearchForm.make_select)
async def make_back(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "🔍 Шаг 1 — Выбери первую букву марки:",
        reply_markup=make_letter_keyboard(),
    )
    await state.set_state(SearchForm.make_letter)
    await callback.answer()


@router.callback_query(F.data.startswith("make_"), SearchForm.make_select)
async def choose_make(callback: CallbackQuery, state: FSMContext):
    make = callback.data.replace("make_", "")  # "make_BMW" → "BMW"
    await state.update_data(make=make)
    await callback.message.edit_text(
        f"🔍 Шаг 3 — Выбери модель <b>{make}</b>:",
        parse_mode="HTML",
        reply_markup=model_select_keyboard(make),
    )
    await state.set_state(SearchForm.model_select)
    await callback.answer()


@router.callback_query(F.data == "model_back", SearchForm.model_select)
async def model_back(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    letter = data.get("letter", "A")
    await callback.message.edit_text(
        f"🔍 Шаг 2 — Выбери марку на букву <b>{letter}</b>:",
        parse_mode="HTML",
        reply_markup=make_select_keyboard(letter),
    )
    await state.set_state(SearchForm.make_select)
    await callback.answer()


@router.callback_query(
    F.data.startswith("model_") | (F.data == "model_all"),
    SearchForm.model_select
)
async def choose_model(callback: CallbackQuery, state: FSMContext):
    if callback.data == "model_all":
        model = ""  # Пустая строка = все модели
    else:
        model = callback.data.replace("model_", "")  # "model_Golf" → "Golf"
    
    await state.update_data(model=model)
    data = await state.get_data()
    make = data.get("make", "")
    
    await callback.message.edit_text(
        f"✅ Марка: <b>{make}</b> | Модель: <b>{model or 'Все'}</b>\n\n"
        f"📅 Шаг 4 — Введи год выпуска <b>от</b>:\n<i>Например: 2018</i>",
        parse_mode="HTML",
        reply_markup=None,
    )
    await state.set_state(SearchForm.year_from)
    await callback.answer()



@router.message(SearchForm.year_from)
async def process_year_from(message: Message, state: FSMContext):
    if message.text == "⏭ Пропустить":
        await state.update_data(year_from=None)
    else:
        if not message.text.isdigit():
            await message.answer("⚠️ Введи число, например: <b>2018</b>", parse_mode="HTML")
            return
        await state.update_data(year_from=int(message.text))

    await message.answer(
        "Шаг 4/6 — Введи <b>год выпуска до</b>:\n"
        "<i>Например: 2022</i>",
        parse_mode="HTML",
        reply_markup=skip_keyboard(),
    )
    await state.set_state(SearchForm.year_to)


@router.message(SearchForm.year_to)
async def process_year_to(message: Message, state: FSMContext):
    if message.text == "⏭ Пропустить":
        await state.update_data(year_to=None)
    else:
        if not message.text.isdigit():
            await message.answer("⚠️ Введи число, например: <b>2022</b>", parse_mode="HTML")
            return
        await state.update_data(year_to=int(message.text))

    await message.answer(
        "Шаг 5/6 — Введи <b>максимальную цену</b> (€):\n"
        "<i>Например: 20000</i>",
        parse_mode="HTML",
        reply_markup=skip_keyboard(),
    )
    await state.set_state(SearchForm.price_max)


@router.message(SearchForm.price_max)
async def process_price_max(message: Message, state: FSMContext):
    if message.text == "⏭ Пропустить":
        await state.update_data(price_max=None)
    else:
        if not message.text.isdigit():
            await message.answer("⚠️ Введи число, например: <b>20000</b>", parse_mode="HTML")
            return
        await state.update_data(price_max=int(message.text))

    await message.answer(
        "Шаг 6/6 — Введи <b>максимальный пробег</b> (км):\n"
        "<i>Например: 150000</i>",
        parse_mode="HTML",
        reply_markup=skip_keyboard(),
    )
    await state.set_state(SearchForm.mileage_max)


@router.message(SearchForm.mileage_max)
async def process_mileage_max(message: Message, state: FSMContext):
    if message.text == "⏭ Пропустить":
        await state.update_data(mileage_max=None)
    else:
        if not message.text.isdigit():
            await message.answer("⚠️ Введи число, например: <b>150000</b>", parse_mode="HTML")
            return
        await state.update_data(mileage_max=int(message.text))

    await message.answer(
        "📍 Шаг 10 — Введи <b>почтовый индекс</b> для поиска по радиусу:\n"
        "<i>Например: 09111 (Хемниц)</i>\n\n"
        "Или нажми Пропустить — будет поиск по всей Германии.",
        parse_mode="HTML",
        reply_markup=skip_keyboard(),
    )
    await state.set_state(SearchForm.zip_code)


# ─────────────────────────────────────────
#  Радиус поиска
# ─────────────────────────────────────────
@router.message(SearchForm.zip_code)
async def process_zip_code(message: Message, state: FSMContext):
    if message.text == "⏭ Пропустить":
        await state.update_data(zip_code=None, radius=0)
        await show_summary(message, state)
        return

    zip_code = message.text.strip()
    if not zip_code.isdigit() or len(zip_code) != 5:
        await message.answer("⚠️ Введи корректный немецкий индекс, например: <b>09111</b>", parse_mode="HTML")
        return

    await state.update_data(zip_code=zip_code)
    await message.answer(
        f"📍 Индекс: <b>{zip_code}</b>\n\nШаг 11 — Выбери радиус поиска:",
        parse_mode="HTML",
        reply_markup=radius_keyboard(),
    )
    await state.set_state(SearchForm.radius)


@router.callback_query(F.data.startswith("radius_"), SearchForm.radius)
async def process_radius(callback: CallbackQuery, state: FSMContext):
    radius = int(callback.data.replace("radius_", ""))
    await state.update_data(radius=radius)
    await callback.message.edit_reply_markup(reply_markup=None)
    await show_summary(callback.message, state)
    await callback.answer()


async def show_summary(message: Message, state: FSMContext):
    """Показывает итоговые параметры поиска."""
    data = await state.get_data()
    zip_info = f"{data.get('zip_code')} (+{data.get('radius')} км)" if data.get('zip_code') else "Вся Германия"
    summary = (
        "✅ <b>Параметры поиска:</b>\n\n"
        f"🚘 Марка:     <b>{data.get('make') or '—'}</b>\n"
        f"🔖 Модель:    <b>{data.get('model') or 'Все'}</b>\n"
        f"📅 Год от:    <b>{data.get('year_from') or '—'}</b>\n"
        f"📅 Год до:    <b>{data.get('year_to') or '—'}</b>\n"
        f"💶 Цена до:   <b>{data.get('price_max') or '—'} €</b>\n"
        f"🛣 Пробег до: <b>{data.get('mileage_max') or '—'} км</b>\n"
        f"📍 Район:     <b>{zip_info}</b>\n"
    )
    await message.answer(
        summary,
        parse_mode="HTML",
        reply_markup=confirm_keyboard(),
    )

# ─────────────────────────────────────────
#  Кнопка "Запустить поиск"
# ─────────────────────────────────────────
@router.callback_query(F.data == "confirm_search")
async def confirm_search(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await save_search(
        user_id=callback.from_user.id,
        make=data["make"],
        model=data["model"],
        year_from=data.get("year_from"),
        year_to=data.get("year_to"),
        price_max=data.get("price_max"),
        mileage_max=data.get("mileage_max"),
        zip_code=data.get("zip_code"),
        radius=data.get("radius", 0),
    )
    await state.clear()
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        "🚀 <b>Поиск запущен!</b>\n\n"
        "Буду следить за AutoScout24 и пришлю уведомление "
        "как только найду подходящее объявление.\n\n"
        "Остановить: /stop",
        parse_mode="HTML",
    )
    await check_new_listings(callback.bot)
    await callback.answer()


# ─────────────────────────────────────────
#  Кнопка "Начать заново"
# ─────────────────────────────────────────
@router.callback_query(F.data == "restart_search")
async def restart_search(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        "🔍 Шаг 1 — Выбери первую букву марки:",
        reply_markup=make_letter_keyboard(),
    )
    await state.set_state(SearchForm.make_letter)
    await callback.answer()

# ─────────────────────────────────────────
#  Выбор сайтов
# ─────────────────────────────────────────
@router.message(Command("sites"))
async def cmd_sites(message: Message):
    user_id = message.from_user.id
    selected = await get_sites(user_id)
    await message.answer(
        "🌐 Выбери сайты для поиска:\n(нажимай чтобы включить/выключить)",
        reply_markup=sites_keyboard(selected),
    )


@router.callback_query(F.data.startswith("site_"))
async def toggle_site(callback: CallbackQuery):
    user_id = callback.from_user.id
    site = callback.data.replace("site_", "")  # "site_mobile" → "mobile"
    selected = await get_sites(user_id)

    if site in selected:
        if len(selected) == 1:
            await callback.answer("⚠️ Должен быть выбран хотя бы один сайт!")
            return
        selected.remove(site)
    else:
        selected.append(site)

    await set_sites(user_id, selected)
    await callback.message.edit_reply_markup(reply_markup=sites_keyboard(selected))
    await callback.answer()


@router.callback_query(F.data == "sites_save")
async def save_sites(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer("✅ Сайты сохранены!")

# ─────────────────────────────────────────
#  Выбор интервала
# ─────────────────────────────────────────
@router.message(Command("interval"))
async def cmd_interval(message: Message):
    user_id = message.from_user.id
    selected = await get_interval(user_id)
    await message.answer(
        "⏱ Выбери интервал проверки объявлений:",
        reply_markup=interval_keyboard(selected),
    )


@router.callback_query(F.data.startswith("interval_"))
async def choose_interval(callback: CallbackQuery):
    user_id = callback.from_user.id
    minutes = int(callback.data.replace("interval_", ""))  # "interval_30" → 30
    await set_interval(user_id, minutes)
    await callback.message.edit_reply_markup(reply_markup=interval_keyboard(minutes))
    await callback.answer(f"✅ Интервал сохранён: {minutes} мин")


# ─────────────────────────────────────────
#  Меню настроек
# ─────────────────────────────────────────
@router.callback_query(F.data == "action_menu")
async def action_menu(callback: CallbackQuery):
    await callback.message.answer(
        "⚙️ <b>Меню настроек</b>",
        parse_mode="HTML",
        reply_markup=settings_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == "menu_language")
async def menu_language(callback: CallbackQuery):
    await callback.message.edit_text(
        "🌍 Выбери язык / Sprache wählen / Choose language:",
        reply_markup=language_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == "menu_sites")
async def menu_sites(callback: CallbackQuery):
    selected = await get_sites(callback.from_user.id)
    await callback.message.edit_text(
        "🌐 Выбери сайты для поиска:",
        reply_markup=sites_keyboard(selected),
    )
    await callback.answer()


@router.callback_query(F.data == "menu_interval")
async def menu_interval(callback: CallbackQuery):
    selected = await get_interval(callback.from_user.id)
    await callback.message.edit_text(
        "⏱ Выбери интервал проверки:",
        reply_markup=interval_keyboard(selected),
    )
    await callback.answer()


@router.callback_query(F.data == "menu_status")
async def menu_status(callback: CallbackQuery):
    search = await get_search(callback.from_user.id)
    if not search:
        await callback.answer("📭 Нет активного поиска!")
        return
    status_icon = "🟢 Активен" if search["is_active"] else "🔴 Остановлен"
    await callback.message.edit_text(
        f"<b>Статус: {status_icon}</b>\n\n"
        f"🚘 {search['make']} {search['model']}\n"
        f"📅 {search['year_from'] or '—'} — {search['year_to'] or '—'}\n"
        f"💶 до {search['price_max'] or '—'} €\n"
        f"🛣 до {search['mileage_max'] or '—'} км",
        parse_mode="HTML",
        reply_markup=settings_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == "menu_close")
async def menu_close(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()


# ─────────────────────────────────────────
#  /stop
# ─────────────────────────────────────────
@router.message(Command("stop"))
async def cmd_stop(message: Message):
    search = await get_search(message.from_user.id)
    if not search or not search["is_active"]:
        await message.answer("ℹ️ У тебя нет активного поиска.")
        return
    await set_active(message.from_user.id, False)
    await message.answer(
        "⛔ <b>Поиск остановлен.</b>\n\n"
        "Настройки сохранены — запустить снова: /search",
        parse_mode="HTML",
    )


# ─────────────────────────────────────────
#  /status
# ─────────────────────────────────────────
@router.message(Command("status"))
async def cmd_status(message: Message):
    search = await get_search(message.from_user.id)
    if not search:
        await message.answer(
            "📭 У тебя ещё нет настроек поиска.\n"
            "Используй /search чтобы начать."
        )
        return

    status_icon = "🟢 Активен" if search["is_active"] else "🔴 Остановлен"
    await message.answer(
        f"<b>Статус поиска: {status_icon}</b>\n\n"
        f"🚘 Марка:     <b>{search['make']}</b>\n"
        f"🔖 Модель:    <b>{search['model']}</b>\n"
        f"📅 Год от:    <b>{search['year_from'] or '—'}</b>\n"
        f"📅 Год до:    <b>{search['year_to'] or '—'}</b>\n"
        f"💶 Цена до:   <b>{search['price_max'] or '—'} €</b>\n"
        f"🛣 Пробег до: <b>{search['mileage_max'] or '—'} км</b>",
        parse_mode="HTML",
    )

# ─────────────────────────────────────────
#  Кнопки под объявлениями
# ─────────────────────────────────────────
@router.callback_query(F.data == "action_stop")
async def action_stop(callback: CallbackQuery):
    await set_active(callback.from_user.id, False)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        "⛔ <b>Поиск остановлен.</b>\n\n"
        "Настройки сохранены — запустить снова: /search",
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "action_refresh")
async def action_refresh(callback: CallbackQuery):
    await callback.answer("🔄 Запускаю проверку...")
    await check_new_listings(callback.bot)


@router.callback_query(F.data == "action_new_search")
async def action_new_search(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        "🔍 Шаг 1 — Выбери первую букву марки:",
        reply_markup=make_letter_keyboard(),
    )
    await state.set_state(SearchForm.make_letter)
    await callback.answer()