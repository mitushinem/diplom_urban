import os
from dotenv import find_dotenv
from loguru import logger
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    BOT_TOKEN: str
    RAPID_API_KEY: str
    DB_HOST: str = Field(default='localhost')
    DB_PORT: int = Field(default=5432)
    DB_USER: str = Field(default='postgres')
    DB_PASS: str
    DB_NAME: str

    @property
    def ADMIN_DATABASE_URL_asyncpg(self):
        return f'postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/postgres'

    @property
    def DATABASE_URL_asyncpg(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    model_config = SettingsConfigDict(env_file=".env")


if not find_dotenv():
    logger.error('Переменные окружения не загружены т.к отсутствует файл .env')
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    # load_dotenv()
    settings = Settings()

DEFAULT_COMMANDS = (
    ('start', 'Запустить бота'),
    ('help', 'Вывести справку'),
    ('lowprice', 'Самые дешевые отели'),
    ('highprice', 'Самые дорогие отели'),
    ('bestdeal', 'Выбрать отели по своим параметрам'),
    ('history', 'История запросов'),
)

HEADERS_HOTEL_API = {
    'content-type': 'application/json',
    'x-rapidapi-host': 'hotels4.p.rapidapi.com',
    'x-rapidapi-key': settings.RAPID_API_KEY,
}

URL_API = {
    'search_v3': 'locations/v3/search',
    'list_v2': 'properties/v2/list',
    'get_detail_v2': 'properties/v2/detail',
}

logger.add(Path.cwd() / 'log' / 'bot_hotels.log', compression='zip',
           rotation='10MB', format='{time} {level} {message}', level='DEBUG')
