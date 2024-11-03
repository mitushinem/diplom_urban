from aiogram.fsm.state import State, StatesGroup


class StateUser(StatesGroup):
    city = State()
    hotel_count = State()
    price_range = State()
    distance_range = State()
    data_in = State()
    data_out = State()
    adults = State()
    foto_load = State()
    foto_count = State()
    result = State()
    calendar_1 = State()
    calendar_2 = State()
