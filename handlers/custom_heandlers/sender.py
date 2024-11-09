import json
from datetime import datetime
from config.config import URL_API, DEFAULT_COMMANDS
from database.db import add_record
from rapid_api.hotels import generate_json_info_hotel, api_request
from aiogram import F
from aiogram.types import InputMediaPhoto, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from pycbrf.toolbox import ExchangeRates

from loader import dp


def date_difference(checkIn, checkOut):
    date1 = datetime.strptime(checkIn, "%Y-%m-%d").date()
    date2 = datetime.strptime(checkOut, "%Y-%m-%d").date()

    return abs((date2 - date1).days)


def get_message(data_from_message: dict) -> list:
    lang = data_from_message['currency']
    price = data_from_message['price']
    dist = 'Mile'
    if lang == 'RUB':
        dist = 'КМ'
    url = 'https://www.hotels.com/h{}.Hotel-Information'.format(data_from_message['id'])
    res = [
        '<b><a href="{}/">{}</a></b>'.format(url, data_from_message['name']),
        '<b>Адрес: </b>{}'.format(data_from_message['location']),
        '<b>Растояние от центра: </b>{} {}'.format(data_from_message['distance'], dist),
        '<b>Стоимость за сутки: </b>{} {}'.format(price, lang),
        '<b>Стоимость за период с {} по {}:</b> {} {}'.format(data_from_message['checkIn'],
                                                              data_from_message['checkOut'],
                                                              str(data_from_message['days'] * price), lang)
    ]
    return res


def print_foto(msg: list, urls_foto: list) -> list:
    media_group = [
        InputMediaPhoto(parse_mode='HTML', media=url, caption='\n'.join(msg) if key == 0 else '')
        for key, url in enumerate(urls_foto)]
    return media_group


@dp.message(F.text == 'Подтвердить')
async def send_message(message: Message, state: FSMContext) -> None:
    name_hotels = {
        'url': []
    }

    reply_remove = ReplyKeyboardRemove()
    await message.answer('Ожидайте, запрос обрабатывается...', reply_markup=reply_remove)

    data = await state.get_data()

    rate = ExchangeRates(datetime.now())

    payload = generate_json_info_hotel(date_dict=data, command=data['command'])

    resolv_data = json.loads(await api_request(method_endswith=URL_API['list_v2'],
                                         method_type='POST',
                                         params=payload))

    list_hotels_info = resolv_data['data']['propertySearch']['properties']

    result = []

    if list_hotels_info:
        for i in list_hotels_info:
            t_dict = dict()
            t_dict['id'] = i.get('id', None)
            t_dict['name'] = i.get('name', None)
            t_dict['currency'] = data['currency']

            if t_dict['id'] is None:
                continue

            # Если россия, то получить текущий курс и умножить
            if t_dict['currency'] == 'RUB':
                t_dict['price'] = round((int(i['price']['lead'].get('amount', 0)) * rate['USD'][-1]))
            else:
                t_dict['price'] = round(i['price']['lead'].get('amount', 0))

            # Расстояние от центра
            if t_dict['currency'] == 'RUB':
                t_dict['distance'] = round((i['destinationInfo']['distanceFromDestination']['value'] * 1.61), 2)
            else:
                t_dict['distance'] = round((i['destinationInfo']['distanceFromDestination']['value']), 2)

            t_dict['checkIn'] = data['checkIn']
            t_dict['checkOut'] = data['checkOut']
            t_dict['days'] = date_difference(data['checkIn'], data['checkOut'])

            payload_v2_detail = {
                'propertyId': t_dict['id']
            }

            get_detail_hotel = json.loads(await api_request(method_endswith=URL_API['get_detail_v2'],
                                                      method_type='POST', params=payload_v2_detail))

            if data['load_image']:
                image_list = get_detail_hotel['data']['propertyInfo']['propertyGallery']['images']
                t_dict['url_foto'] = []
                for i_img in range(int(data['foto_count'])):
                    t_dict['url_foto'].append(image_list[i_img]['image']['url'])

            get_summary = get_detail_hotel['data']['propertyInfo']['summary']
            t_dict['location'] = ', '.join((get_summary['location']['address']['city'],
                                            get_summary['location']['address']['addressLine']))

            result.append(t_dict)

    for i_msg in result:
        msg = get_message(i_msg)
        if data['load_image']:
            media_data = print_foto(msg, urls_foto=i_msg['url_foto'])
            await message.bot.send_media_group(chat_id=message.from_user.id, media=media_data)
        else:
            await message.answer('\n'.join(msg), disable_web_page_preview=True)

        name_hotels['url'].append(msg[0])


    await add_record(telegram_id=message.from_user.id,
                  command=data['command'],
                  hotels='\n'.join(name_hotels['url']),
                  city=data['city'])

    await state.clear()

    text = [f'/<b>{command}</b> - {desk}' for command, desk in DEFAULT_COMMANDS]
    await message.answer('Запрос успешно выполнен!')
    await message.answer('\n'.join(text))
