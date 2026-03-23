import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from database import init_db
from handlers import router
from scheduler import create_scheduler
from database import get_all_active_searches
from keyboards import listing_keyboard

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
print("=== СТАРТ ===")
BOT_TOKEN = os.getenv("BOT_TOKEN")
print(f"TOKEN = {BOT_TOKEN}")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)

async def set_commands(bot: Bot):
    """Устанавливает меню команд бота."""
    commands = [
        BotCommand(command="start",  description="🌍 Выбрать язык / Start"),
        BotCommand(command="search", description="🔍 Новый поиск"),
        BotCommand(command="stop",   description="⛔ Остановить поиск"),
        BotCommand(command="status", description="📊 Статус поиска"),
        BotCommand(command="sites", description="🌐 Выбор сайтов поиска"),
        BotCommand(command="interval", description="⏱ Интервал проверки"),
    ]
    await bot.set_my_commands(commands)

async def main():
    print("=== ВОШЛИ В MAIN ===")
    print("🗄 Инициализация базы данных...")
    await init_db()

    print("⏰ Запуск планировщика...")
    scheduler = create_scheduler(bot)
    scheduler.start()

    print("🚗 CarHunter Bot запущен!")

    await set_commands(bot)

    # Уведомляем пользователей с активным поиском о рестарте
    searches = await get_all_active_searches()
    for search in searches:
        await bot.send_message(
            chat_id=search["user_id"],
            text=(
                f"🟢 <b>Бот перезапущен!</b>\n\n"
                f"Твой поиск активен:\n"
                f"🚘 {search['make']} {search['model']}\n\n"
                f"Следующая проверка запустится автоматически."
            ),
            parse_mode="HTML",
            reply_markup=listing_keyboard(),
        )

    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Бот остановлен из-за ошибки: {e}")
    finally:
        print("🛑 Бот остановлен")
        scheduler.shutdown()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())