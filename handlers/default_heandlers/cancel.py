from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from config.config import DEFAULT_COMMANDS

router_cancel = Router()


@router_cancel.message(F.text == 'Отмена')
async def bot_cancel(message: Message, state: FSMContext):
    await state.clear()
    reply_remove = ReplyKeyboardRemove()
    await message.answer('Отмена запроса, повторите заново', reply_markup=reply_remove)
    text = [f'/<b>{command}</b> - {desk}' for command, desk in DEFAULT_COMMANDS]
    await message.answer('\n'.join(text))
