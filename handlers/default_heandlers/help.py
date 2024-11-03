from config.config import DEFAULT_COMMANDS
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router

router_help = Router()

@router_help.message(Command('help'))
async def bot_help(message: Message):
    text = [f'/<b>{command}</b> - {desk}' for command, desk in DEFAULT_COMMANDS]
    await message.answer('\n'.join(text))


