from datetime import datetime, timedelta
from aiogram import F
from aiogram.filters.callback_data import CallbackData
from keyboards.reply.reply_keyboard import accept_keyboard
from loader import dp
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from states.state import StateUser
from aiogram_calendar import SimpleCalendarCallback, get_user_locale, SimpleCalendar


#
# @bot.callback_query_handler(func=lambda call: call.data == 'start')
# def callback_start(call: CallbackQuery) -> None:
#     """
#     Обработчик нажатия по отмена
#     """
#     bot.delete_state(call.from_user.id, call.message.chat.id)
#     bot.delete_message(call.message.chat.id, call.message.message_id)
#     msg = bot.send_message(call.from_user.id, 'Операция отменена. Повторите запрос с новыми параметрами поиска')
#     bot_help(msg)
#
#


@dp.callback_query(F.data.startswith('_state_'))
async def callback_city(call: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик нажатия по кнопке выбора города
    """
    # bot.delete_message(call.message.chat.id, call.message.message_id)

    city = call.data.replace('_state_', '').split('|')
    await state.update_data(destinationId=city[1], city=city[0])

    data = await state.get_data()

    if data['command'].endswith('price'):
        await state.set_state(StateUser.hotel_count)
        await call.message.answer('Сколько отелей вывести в результатах поиска?')
        await call.answer()
    elif data['command'].endswith('bestdeal'):
        await state.set_state(StateUser.price_range)
        await call.message.answer('Введите диапозон цен через пробел?')
        await call.answer()


@dp.callback_query(SimpleCalendarCallback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: CallbackData,
                                  state: FSMContext) -> None:
    if await state.get_state() == StateUser.calendar_1:

        calendar = SimpleCalendar(
            locale=await get_user_locale(callback_query.from_user), show_alerts=True
        )
        calendar.set_dates_range(datetime.now(), datetime(datetime.now().year + 2, 12, 31))
        selected, date = await calendar.process_selection(callback_query, callback_data)
        if selected:
            await state.set_state(StateUser.calendar_2)
            await state.update_data(checkIn=date.strftime('%Y-%m-%d'), data_checkIn=date)
            await callback_query.message.answer(
                f'Выберите дату выезда:',
                reply_markup=await SimpleCalendar().start_calendar()
            )


    elif await state.get_state() == StateUser.calendar_2:
        data = await state.get_data()

        calendar = SimpleCalendar(
            locale=await get_user_locale(callback_query.from_user), show_alerts=True
        )
        calendar.set_dates_range(data['data_checkIn'] + timedelta(days=1),
                                 datetime(datetime.now().year + 2, 12, 31))
        selected, date = await calendar.process_selection(callback_query, callback_data)
        if selected:
            await state.set_state(StateUser.adults)
            await state.update_data(checkOut=date.strftime('%Y-%m-%d'), data_checkOut=date)
            await callback_query.message.answer(f'Сколько человек будет проживать в номере?')


@dp.callback_query(F.data.endswith('_foto'))
async def callback_foto_download(call: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик нажатия по кнопке выбора показа фото в выдаче или нет
    """
    match call.data:
        case 'yes_foto':
            await state.update_data(load_image=True)
            await state.set_state(StateUser.foto_count)
            await call.message.answer('Сколько фотографий отеля загружать, но не более 5?')
            await call.answer()
        case 'no_foto':
            await state.update_data(load_image=False)
            await state.set_state(StateUser.result)

            await call.message.answer('Для продолжения требуется подтверждение...',
                                      reply_markup=accept_keyboard())

#
# @bot.callback_query_handler(func=lambda call: call.data.startswith('is_'))
# def callback_history(call: CallbackQuery) -> None:
#     try:
#         bot.delete_message(call.message.chat.id, call.message.message_id)
#         match call.data:
#             case 'is_today':
#                 for i_msg in select_all_record_for_days(call.from_user.id):
#                     bot.send_message(call.from_user.id, '\n'.join(get_message_history(i_msg)),
#                                      disable_web_page_preview=True)
#             case 'is_week':
#                 pass
#                 for i_msg in select_all_record_for_days(call.from_user.id, days=7):
#                     bot.send_message(call.from_user.id, '\n'.join(get_message_history(i_msg)),
#                                      disable_web_page_preview=True)
#             case 'is_month':
#                 for i_msg in select_all_record_for_days(call.from_user.id, days=30):
#                     bot.send_message(call.from_user.id, '\n'.join(get_message_history(i_msg)),
#                                      disable_web_page_preview=True)
#             case 'is_all':
#                 for i_msg in select_all_record(call.from_user.id):
#                     bot.send_message(call.from_user.id, '\n'.join(get_message_history(i_msg)),
#                                      disable_web_page_preview=True)
#             case 'is_delete':
#                 delete_all_record(call.from_user.id)
#     except Exception as err:
#         bot.send_message(call.from_user.id, err)
