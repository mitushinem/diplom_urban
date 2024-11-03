from aiogram.types import Message
from aiogram.filters import Command
# from database.db import add_user
from aiogram import Router
from states.state import StateUser
from aiogram.fsm.context import FSMContext

router_highprice = Router()


@router_highprice.message(Command('highprice'))
async def bot_lowprice(message: Message, state: FSMContext) -> None:
    # add_user(message.from_user.full_name, message.from_user.id)

    await state.set_state(StateUser.city)
    await state.update_data(command=message.text)
    await message.answer('<b>В каком городе будем искать отели?</b>')
