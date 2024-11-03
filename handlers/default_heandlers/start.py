from aiogram.types import Message
# from database.db import add_user
from aiogram import Router
from aiogram.filters import CommandStart

router_start = Router()

@router_start.message(CommandStart())
async def bot_start(message: Message):

    #TODO Добавление пользователя в базу если его нет
    # add_user(message.from_user.full_name, message.from_user.id)

    await message.reply(f"Привет, {message.from_user.full_name}! \n"
                        f"Для того что-бы узнать я умею набери /help")
