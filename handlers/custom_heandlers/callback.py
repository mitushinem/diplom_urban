from datetime import datetime, timedelta
from aiogram import F
from aiogram.filters.callback_data import CallbackData
from database.db import select_all_record, select_all_record_for_days, delete_all_record
from handlers.custom_heandlers.history import get_message_history
from keyboards.reply.reply_keyboard import accept_keyboard
from loader import dp
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from states.state import StateUser
from aiogram_calendar import SimpleCalendarCallback, get_user_locale, SimpleCalendar
from config.config import logger, DEFAULT_COMMANDS
from utils.utils import get_data_for_message_history


@dp.callback_query(F.data == 'start')
async def callback_start(call: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик нажатия по отмена
    """
    await state.clear()
    text = [f'/<b>{command}</b> - {desk}' for command, desk in DEFAULT_COMMANDS]
    await call.message.answer('Операция отменена!')
    await call.message.answer('\n'.join(text))
    await call.answer()


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
    elif data['command'].endswith('deal'):
        await state.set_state(StateUser.price_range)
        await call.message.answer('Введите диапазон цен через пробел?')
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
        case 'no_foto':
            await state.update_data(load_image=False)
            await state.set_state(StateUser.result)

            await call.message.answer('Для продолжения требуется подтверждение...',
                                      reply_markup=accept_keyboard())
    await call.answer()


@dp.callback_query(F.data.startswith('is_'))
async def callback_history(call: CallbackQuery) -> None:
    try:
        match call.data:
            case 'is_today':
                all_record = await select_all_record_for_days(call.from_user.id)
                if all_record is not None:
                    for rec in all_record:
                        data = get_data_for_message_history(rec)
                        await call.message.answer('\n'.join(get_message_history(data)), disable_web_page_preview=True)
                else:
                    await call.message.answer(
                        f'У пользователя с telegram_id: {call.from_user.id} нет записей в истории')
                    logger.info(f'У пользователя с telegram_id: {call.from_user.id} нет записей в истории')
                await call.answer()

            case 'is_week':
                all_record = await select_all_record_for_days(call.from_user.id, days=7)
                if all_record is not None:
                    for rec in all_record:
                        data = get_data_for_message_history(rec)
                        await call.message.answer('\n'.join(get_message_history(data)), disable_web_page_preview=True)
                else:
                    await call.message.answer(
                        f'У пользователя с telegram_id: {call.from_user.id} нет записей в истории')
                    logger.info(f'У пользователя с telegram_id: {call.from_user.id} нет записей в истории')
                await call.answer()

            case 'is_month':
                all_record = await select_all_record_for_days(call.from_user.id, days=30)
                if all_record is not None:
                    for rec in all_record:
                        data = get_data_for_message_history(rec)
                        await call.message.answer('\n'.join(get_message_history(data)), disable_web_page_preview=True)
                else:
                    await call.message.answer(
                        f'У пользователя с telegram_id: {call.from_user.id} нет записей в истории')
                    logger.info(f'У пользователя с telegram_id: {call.from_user.id} нет записей в истории')

                await call.answer()

            case 'is_all':
                all_record = await select_all_record(call.from_user.id)
                if all_record is not None:
                    for rec in all_record:
                        data = get_data_for_message_history(rec)
                        await call.message.answer('\n'.join(get_message_history(data)), disable_web_page_preview=True)
                else:
                    await call.message.answer(
                        f'У пользователя с telegram_id: {call.from_user.id} нет записей в истории')
                    logger.info(f'У пользователя с telegram_id: {call.from_user.id} нет записей в истории')

                await call.answer()

            case 'is_delete':
                await delete_all_record(call.from_user.id)
                await call.message.answer(f'Все записи успешно удалены')
                logger.info(f'Все записи для пользователя с telegram_id: {call.from_user.id} успешно удалены')

        await call.message.answer('Запрос выполнен')

    except Exception as err:
        await call.message.answer(err.__str__())
        await call.answer()
        logger.error(err)
