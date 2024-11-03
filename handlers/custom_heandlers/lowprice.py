from config.config import logger
from filters.custom import IsCityNameCorrect, IsDigitCorrectFilter
# from database.db import add_user
from rapid_api.hotels import get_id_destinations
from keyboards.inline.inline_keyboard import *
from keyboards.reply.reply_keyboard import accept_keyboard
from states.state import StateUser
from utils.utils import is_lang
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import Router
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback

router_lowprice = Router()


@router_lowprice.message(Command('lowprice'))
async def bot_lowprice(message: Message, state: FSMContext) -> None:
    # add_user(message.from_user.full_name, message.from_user.id)
    await state.set_state(StateUser.city)
    await state.update_data(command=message.text)
    await message.answer('<b>В каком городе будем искать отели?</b>')


@router_lowprice.message(IsCityNameCorrect(), StateUser.city)
async def get_city(message: Message, state: FSMContext) -> None:
    """
    Получение вариантов поиска по запросу, формирование keyboard с вариантами городов
    """
    lang = is_lang(message.text)
    await state.update_data(city=message.text,
                            locale=lang[0],
                            currency=lang[1])

    data = await state.get_data()

    match data['command']:
        case '/lowprice':
            await state.update_data(sort='PRICE_LOW_TO_HIGH')
        case '/highprice':
            await state.update_data(sort='RECOMMENDED')
        case '/bestdeal':
            await state.update_data(sort='DISTANCE')

    await message.answer("<b>Пожалуйста подождите. Запрос выполняется...</b>")

    id_destinations = get_id_destinations(query=message.text, locale=lang)
    if id_destinations:
        await message.answer(f'По запросу <b>"{message.text}"</b> найдены варианты:\n'
                             f'Ознакомтесь с предложенными вариантами и выберите наиболее подходящий',
                             reply_markup=keyboard_gen_id_destinations(id_destinations))
    else:
        # TODO поправить reply_markup=keyboard_back()
        await message.answer('По вашему запросу ничего не найдено. Повторите запрос заново',
                             reply_markup=keyboard_back())
        await state.clear()


@router_lowprice.message(IsDigitCorrectFilter(1, 25), StateUser.hotel_count)
async def get_hotel_count(message: Message, state: FSMContext) -> None:
    await state.update_data(resultsSize=message.text)
    await state.set_state(StateUser.calendar_1)
    await message.answer("Выберите дату начала проживания:", reply_markup=
    await SimpleCalendar().start_calendar())


@router_lowprice.message(IsDigitCorrectFilter(1, 5), StateUser.adults)
async def get_rooms_count(message: Message, state: FSMContext) -> None:
    await state.update_data(adults=message.text)
    await state.set_state(StateUser.foto_load)
    await message.answer('Показать фотографии отелей?', reply_markup=keyboard_foto_check())


@router_lowprice.message(IsDigitCorrectFilter(1, 5), StateUser.foto_count)
async def get_foto_count(message: Message, state: FSMContext) -> None:
    await state.update_data(foto_count=message.text)
    await state.set_state(StateUser.result)

    await message.answer('Для продолжения требуется подтверждение...',
                         reply_markup=accept_keyboard())
