from aiogram.types import Message
from database.db import set_user
from aiogram import Router
from aiogram.filters import CommandStart

router_start = Router()


@router_start.message(CommandStart())
async def bot_start(message: Message):
    await set_user(telegram_id=message.from_user.id, name=message.from_user.full_name)

    await message.reply(f"Привет, {message.from_user.full_name}! \n"
                        f"Для того что-бы узнать я умею набери /help")
