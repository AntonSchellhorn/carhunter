from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from aiogram import Bot

from database import get_all_active_searches, add_seen_listing, update_last_checked
import time
from keyboards import listing_keyboard
from scraper import scrape_autoscout24, scrape_mobile_de



async def check_new_listings(bot: Bot):
    """
    Главная функция планировщика.
    Запускается каждые 30 минут.
    Проходит по всем активным поискам и отправляет новые объявления.
    """
    print("⏰ Запуск проверки новых объявлений...")

    # Получаем всех пользователей у которых поиск активен
    searches = await get_all_active_searches()
    print(f"👥 Активных поисков: {len(searches)}")

    for search in searches:

        # Проверяем — пришло ли время для этого пользователя
        interval_minutes = search.get("interval") or 30
        last_checked = search.get("last_checked_at") or 0
        elapsed = time.time() - last_checked
        if elapsed < interval_minutes * 60:
            print(f"⏳ Пользователь {search['user_id']}: ещё {int((interval_minutes * 60 - elapsed) / 60)} мин до проверки")
            continue

        await update_last_checked(search["user_id"])

        user_id = search["user_id"]

        # Определяем какие сайты выбрал пользователь
        sites = search.get("sites") or "autoscout24"

        listings = []

        # Запускаем парсер для каждого выбранного сайта
        if "autoscout24" in sites:
            as24 = await scrape_autoscout24(
                make=search["make"],
                model=search["model"],
                year_from=search["year_from"],
                year_to=search["year_to"],
                price_max=search["price_max"],
                mileage_max=search["mileage_max"],
                zip_code=search.get("zip_code"),
                radius=search.get("radius"),
            )
            listings.extend(as24)

        if "mobile" in sites:
            # Mobile.de — минимальный интервал 30 минут (защита от блокировки)
            MOBILE_MIN_INTERVAL = 30 * 60
            last_mobile = search.get("last_mobile_checked_at") or 0
            elapsed_mobile = time.time() - last_mobile

            if elapsed_mobile >= MOBILE_MIN_INTERVAL:
                mob = await scrape_mobile_de(
                    make=search["make"],
                    model=search["model"],
                    year_from=search["year_from"],
                    year_to=search["year_to"],
                    price_max=search["price_max"],
                    mileage_max=search["mileage_max"],
                    zip_code=search.get("zip_code"),
                    radius=search.get("radius"),
                )
                listings.extend(mob)
            else:
                print(f"⏳ Mobile.de: ещё {int((MOBILE_MIN_INTERVAL - elapsed_mobile) / 60)} мин до проверки")

        new_count = 0

        for listing in listings:
            # Проверяем — видели ли мы уже это объявление?
            is_new = await add_seen_listing(user_id, listing["id"])

            if is_new:
                new_count += 1
                # Отправляем уведомление пользователю
                await bot.send_message(
                    chat_id=user_id,
                    text=(
                        f"🚗 <b>Новое объявление!</b>\n\n"
                        f"📌 {listing['title']}\n"
                        f"💶 Цена: <b>{listing['price']}</b>\n"
                        f"🛣 Пробег: <b>{listing['mileage']}</b>\n"
                        f"📅 Год: <b>{listing['year']}</b>\n\n"
                        f"🔗 <a href='{listing['url']}'>Открыть объявление</a>"
                    ),
                    parse_mode="HTML",
                    disable_web_page_preview=False,
                    reply_markup=listing_keyboard(),  # ← вот эта строка
                )

        print(f"✅ Пользователь {user_id}: новых объявлений — {new_count}")


def create_scheduler(bot: Bot) -> AsyncIOScheduler:
    """
    Создаёт и возвращает планировщик.
    Запускается каждую минуту — но проверяет только тех пользователей,
    у которых вышел их личный интервал.
    """
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        check_new_listings,
        trigger="interval",
        minutes=5,
        kwargs={"bot": bot},
        next_run_time=datetime.now(),
    )

    return scheduler