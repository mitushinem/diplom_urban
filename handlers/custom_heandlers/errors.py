from aiogram.types import Message
from filters.custom import IsCityNameCorrect, IsPriceCorrect, IsDigitCorrectFilter
from handlers.custom_heandlers.bestdeal import router_bestdeal
from handlers.custom_heandlers.lowprice import router_lowprice
from states.state import StateUser


@router_lowprice.message(~IsCityNameCorrect(), StateUser.city)
async def get_city_err(message: Message) -> None:
    await message.answer('Введите корректное название города')


@router_lowprice.message(~IsDigitCorrectFilter(1, 25), StateUser.hotel_count)
async def get_hotel_count_err(message: Message) -> None:
    await message.answer('Допустимое значение для количества выводимых отелей от 1 до 25')


@router_lowprice.message(~IsDigitCorrectFilter(1, 5), StateUser.adults)
async def get_hotel_count_err(message: Message) -> None:
    await message.answer('Допустимое значение для количества проживающих в отеле от 1 до 5')


@router_lowprice.message(~IsDigitCorrectFilter(1, 5), StateUser.foto_count)
async def get_foto_count_err(message: Message) -> None:
    await message.answer('Допустимое значение от 1 до 5 фотографий')


@router_bestdeal.message(~IsPriceCorrect(), StateUser.price_range)
async def get_price_range_err(message: Message) -> None:
    await message.answer('Введите диапазон цен через пробел')
