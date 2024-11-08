import re
from datetime import datetime
from typing import Tuple, Union


def is_lang(message: str) -> Union[Tuple[str, str], None]:
    """
    Определение языка ввода и валюты
    """
    if re.search(r'[а-яА-Я\- ]+', message) is not None:
        return 'ru_RU', 'RUB'
    elif re.search(r'[a-zA-Z\- ]+', message) is not None:
        return 'en_US', 'USD'


def parse_datetime_string(date_str):
    # Регулярное выражение для извлечения компонентов даты и времени
    match = re.match(r"datetime\.datetime\((\d+), (\d+), (\d+), (\d+), (\d+), (\d+), (\d+)\)", date_str)
    if match:
        year, month, day, hour, minute, second = map(int, match.groups())
        # Создаем объект datetime
        return datetime(year, month, day, hour, minute, second)
    else:
        raise ValueError("Неправильный формат строки")


def get_data_for_message_history(rec):
    data = {
        'created_at': rec.created_at,
        'command': rec.command,
        'city': rec.city,
        'hotels': rec.hotels,
    }

    return data
