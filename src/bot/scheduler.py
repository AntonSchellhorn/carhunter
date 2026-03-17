from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from aiogram import Bot

from database import get_all_active_searches, add_seen_listing
from keyboards import listing_keyboard
from scraper import scrape_autoscout24



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
        user_id = search["user_id"]

        # Запускаем парсер с параметрами этого пользователя
        listings = await scrape_autoscout24(
            make=search["make"],
            model=search["model"],
            year_from=search["year_from"],
            year_to=search["year_to"],
            price_max=search["price_max"],
            mileage_max=search["mileage_max"],
        )

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
    """
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        check_new_listings,
        trigger="interval",
        minutes=30,
        kwargs={"bot": bot},
        next_run_time=datetime.now(),
    )

    return scheduler