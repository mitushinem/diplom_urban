from aiogram.types import Message

from database.db import set_user
from keyboards.inline.inline_keyboard import keyboard_history
from aiogram import Router
from aiogram.filters import Command


router_history = Router()


def get_message_history(history_data) -> list:

    msg = [
        '<b>Дата запроса: </b>{}'.format(history_data['created_at']),
        '<b>Команда: </b>{}\n'.format(history_data['command']),
        '<b>Город: </b>{}\n'.format(history_data['city']),
        '<b>Список найденных отелей:\n</b>',
        '{}'.format(history_data['hotels'])
    ]
    return msg


@router_history.message(Command('history'))
async def bot_history(message: Message) -> None:
    await set_user(message.from_user.id, message.from_user.full_name)
    await message.answer('Выберите вариант поиска запросов', reply_markup=keyboard_history())
