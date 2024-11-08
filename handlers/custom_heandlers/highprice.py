from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router
from database.db import set_user
from states.state import StateUser
from aiogram.fsm.context import FSMContext

router_highprice = Router()


@router_highprice.message(Command('highprice'))
async def bot_lowprice(message: Message, state: FSMContext) -> None:
    await set_user(message.from_user.id, message.from_user.full_name)
    await state.set_state(StateUser.city)
    await state.update_data(command=message.text)
    await message.answer('<b>В каком городе будем искать отели?</b>')
