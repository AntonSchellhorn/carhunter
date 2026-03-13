from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "🚗 Привет! Я CarHunter Bot!\n\n"
        "Я ищу автомобили на AutoScout24 24/7 "
        "и сообщаю когда нахожу выгодное предложение.\n\n"
        "Команды:\n"
        "/search — настроить поиск\n"
        "/stop — остановить поиск\n"
        "/status — статус поиска"
    )