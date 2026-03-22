from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from scheduler import check_new_listings
from keyboards import confirm_keyboard, skip_keyboard, listing_keyboard, language_keyboard, sites_keyboard
from database import save_search, get_search, set_active, set_language, get_language, get_sites, set_sites
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
        "🔍 Настраиваем поиск!\n\n"
        "Шаг 1/6 — Введи <b>марку</b> автомобиля:\n"
        "<i>Например: BMW, Volkswagen, Toyota</i>",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(SearchForm.make)


@router.message(SearchForm.make)
async def process_make(message: Message, state: FSMContext):
    await state.update_data(make=message.text.strip())
    await message.answer(
        "Шаг 2/6 — Введи <b>модель</b>:\n"
        "<i>Например: 3 Series, Golf, Camry</i>",
        parse_mode="HTML",
    )
    await state.set_state(SearchForm.model)


@router.message(SearchForm.model)
async def process_model(message: Message, state: FSMContext):
    await state.update_data(model=message.text.strip())
    await message.answer(
        "Шаг 3/6 — Введи <b>год выпуска от</b>:\n"
        "<i>Например: 2018</i>",
        parse_mode="HTML",
        reply_markup=skip_keyboard(),
    )
    await state.set_state(SearchForm.year_from)


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

    data = await state.get_data()
    summary = (
        "✅ <b>Параметры поиска:</b>\n\n"
        f"🚘 Марка:     <b>{data['make']}</b>\n"
        f"🔖 Модель:    <b>{data['model']}</b>\n"
        f"📅 Год от:    <b>{data.get('year_from') or '—'}</b>\n"
        f"📅 Год до:    <b>{data.get('year_to') or '—'}</b>\n"
        f"💶 Цена до:   <b>{data.get('price_max') or '—'} €</b>\n"
        f"🛣 Пробег до: <b>{data.get('mileage_max') or '—'} км</b>\n"
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
        "🔄 Начинаем заново!\n\n"
        "Шаг 1/6 — Введи <b>марку</b> автомобиля:",
        parse_mode="HTML",
    )
    await state.set_state(SearchForm.make)
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
        "🔍 Настраиваем новый поиск!\n\n"
        "Шаг 1/6 — Введи <b>марку</b> автомобиля:\n"
        "<i>Например: BMW, Volkswagen, Toyota</i>",
        parse_mode="HTML",
    )
    await state.set_state(SearchForm.make)
    await callback.answer()