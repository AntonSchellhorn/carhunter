import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import router

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)

async def main():
    print("🚗 CarHunter Bot запущен!")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Бот остановлен из-за ошибки: {e}")
    finally:
        print("🛑 Бот остановлен")
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())