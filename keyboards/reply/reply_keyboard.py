from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def accept_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Подтвердить'), KeyboardButton(text='Отмена')]
    ], resize_keyboard=True)
