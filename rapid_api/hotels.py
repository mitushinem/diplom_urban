from config.config import HEADERS_HOTEL_API, URL_API, logger
from typing import Union
import httpx


async def api_request(method_endswith, params: dict, method_type: str):
    url_api = f'https://hotels4.p.rapidapi.com/{method_endswith}'

    async with httpx.AsyncClient() as client:
        if method_type == 'GET':
            return await get_request(client, url=url_api, params=params)
        elif method_type == 'POST':
            return await post_request(client, url=url_api, payload=params)


async def get_request(client: httpx.AsyncClient, url: str, params: dict):
    """
    Асинхронный GET запрос на сервер
    """
    try:
        response = await client.get(url, headers=HEADERS_HOTEL_API, params=params, timeout=15)
        response.raise_for_status()  # Вызывает исключение для статусов, отличных от 2xx
        return response.text
    except httpx.RequestError as err:
        logger.error(f"Ошибка при выполнении GET запроса {err}")
        return None


async def post_request(client: httpx.AsyncClient, url: str, payload: dict):
    """
    Асинхронный POST запрос на сервер
    """
    try:
        response = await client.post(url, headers=HEADERS_HOTEL_API, json=payload, timeout=15)
        response.raise_for_status()  # Вызывает исключение для статусов, отличных от 2xx
        return response.text
    except httpx.RequestError as err:
        logger.error(f"Ошибка при выполнении POST запроса {err}")
        return None


async def get_id_destinations(query: str, locale: tuple) -> list[tuple]:
    """
    Асинхронный метод получает список возможных городов по запросу пользователя.
    Поиск по двум локалям.

    :param query: str строка запроса поиска от пользователя
    :param locale: Tuple (локаль, валюта)

    :return List
    Пример результата работы метода:
    ('Москва', '1153093'), ('Центр Москвы', '10565407'), ('Измайлово', '10779356'), ('Арбат', '1665959')
    """
    try:
        query_json = {
            'q': query,
            'locale': locale[0],
        }

        # Асинхронный запрос с использованием httpx
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://hotels4.p.rapidapi.com/{URL_API['search_v3']}", params=query_json,
                                        headers=HEADERS_HOTEL_API, timeout=15)

            response.raise_for_status()  # Вызывает исключение для статусов, отличных от 2xx
            data = response.json()

            if data.get('sr'):
                return [(i_elem['regionNames']['shortName'], i_elem['gaiaId']) for i_elem in data['sr']
                        if i_elem['type'] == 'CITY']
            else:
                raise ValueError(f'Регион "{query}" не найден. Выполнение невозможно')

    except httpx.RequestError as err:
        logger.error(f"Ошибка запроса: {err}")
    except ValueError as err:
        logger.error(f"Ошибка обработки данных: {err}")
    except Exception as err:
        logger.error(f"Неизвестная ошибка: {err}")


def generate_json_info_hotel(date_dict: dict, command: Union[str, None] = None) -> dict:
    payload = {
        'currency': date_dict['currency'],
        'eapid': 1,
        'locale': date_dict['locale'],
        'destination': {'regionId': date_dict['destinationId']},
        'checkInDate': {
            'day': int(date_dict['data_checkIn'].day),
            'month': int(date_dict['data_checkIn'].month),
            'year': int(date_dict['data_checkIn'].year)
        },
        'checkOutDate': {
            'day': int(date_dict['data_checkOut'].day),
            'month': int(date_dict['data_checkOut'].month),
            'year': int(date_dict['data_checkOut'].year)
        },
        'rooms': [
            {
                'adults': int(date_dict['adults']),
            }
        ],
        'resultsStartingIndex': 0,
        'resultsSize': int(date_dict['resultsSize']),
        'sort': date_dict['sort'],
        'filters': {
            'availableFilter': 'SHOW_AVAILABLE_ONLY',
        }
    }
    if command == '/bestdeal':
        payload['filters']['price'] = {'max': date_dict['priceMax'], 'min': date_dict['priceMin']}

    return payload
