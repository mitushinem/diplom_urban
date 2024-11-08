from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import Router

from database.db import set_user
from filters.custom import IsPriceCorrect
from states.state import StateUser


router_bestdeal = Router()


@router_bestdeal.message(Command('bestdeal'))
async def bot_bestdeal(message: Message, state: FSMContext) -> None:
    await set_user(message.from_user.id, message.from_user.full_name)
    await state.set_state(StateUser.city)
    await state.update_data(command=message.text)
    await message.answer('<b>В каком городе будем искать отели?</b>')

@router_bestdeal.message(IsPriceCorrect(), StateUser.price_range)  #
async def get_price_range(message: Message, state: FSMContext) -> None:
    """
    Получение диапозона цен для поиска
    """

    priceMin = message.text.split(' ')[0]
    priceMax = message.text.split(' ')[1]

    await state.set_state(StateUser.hotel_count)
    await state.update_data(priceMin=priceMin, priceMax=priceMax)
    await message.answer('<b>Сколько отелей вывести в результатах поиска?</b>')


