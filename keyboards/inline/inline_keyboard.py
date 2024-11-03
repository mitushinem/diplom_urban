from typing import List, Tuple
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def keyboard_gen_id_destinations(id_destinations: List[Tuple]) -> InlineKeyboardMarkup:
    """
    Генерация Inline клавиатуры с вариантами городов при вводе запроса пользователя
    """

    inline_keyboard_list = []
    for elem in id_destinations:
        key = InlineKeyboardButton(text=elem[0], callback_data='|'.join(('_state_' + elem[0], elem[1])))
        inline_keyboard_list.append([key])
    key = InlineKeyboardButton(text="Отмена операции", callback_data='start')
    inline_keyboard_list.append([key])

    gen_keyboard = InlineKeyboardMarkup(inline_keyboard=[*inline_keyboard_list])

    return gen_keyboard


def keyboard_back(text_message: str = 'Отмена операции') -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой Отмена
    """
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Отмена', callback_data='start')]])


def keyboard_foto_check() -> InlineKeyboardMarkup:
    """
    Клавиатура выбора да\нет для загрузки фото в выдаче
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Да', callback_data='yes_foto'),
         InlineKeyboardButton(text='Нет', callback_data='no_foto')]
    ])

#
# def keyboard_history() -> InlineKeyboardMarkup:
#     """
#     Генерация Inline клавиатуры с вариантами городов при вводе запроса пользователя
#     """
#     keyboard = InlineKeyboardMarkup()
#
#     key_1 = InlineKeyboardButton(text='За сегодня', callback_data='is_today')
#     key_2 = InlineKeyboardButton(text='За неделю', callback_data='is_week')
#     key_3 = InlineKeyboardButton(text='За месяц', callback_data='is_month')
#     key_2_1 = InlineKeyboardButton(text='Вся история', callback_data='is_all')
#     key_3_1 = InlineKeyboardButton(text='Удалить всю историю', callback_data='is_delete')
#
#     keyboard.add(key_1, key_2, key_3)
#     keyboard.add(key_2_1)
#     keyboard.add(key_3_1)
#
#     return keyboard
