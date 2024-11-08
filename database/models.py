import asyncpg
from loguru import logger
from sqlalchemy import ForeignKey, text, BigInteger, UniqueConstraint, PrimaryKeyConstraint, ForeignKeyConstraint, Index
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from datetime import datetime
from typing import Annotated
from config.config import settings

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
user_fk = Annotated[BigInteger, mapped_column(ForeignKey('users.user_id', ondelete='CASCADE', onupdate='CASCADE'))]


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('user_id', name='user_fk'),
        UniqueConstraint('telegram_id')
    )

    user_id: Mapped[intpk]
    name: Mapped[str]
    telegram_id = mapped_column(BigInteger, unique=True, nullable=False)
    created_at: Mapped[created_at]
    history = relationship('History', back_populates='user')


class History(Base):
    __tablename__ = 'history'

    query_id: Mapped[intpk]
    user_id: Mapped[user_fk]
    created_at: Mapped[created_at]
    command: Mapped[str]
    city: Mapped[str]
    hotels: Mapped[str]
    user = relationship('User', back_populates='history')


engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
    pool_size=20,
    max_overflow=10,
)

async_session = async_sessionmaker(bind=engine)


async def create_database_if_not_exists():
    # Функция для создания базы данных, если она не существует
    conn = await asyncpg.connect(settings.ADMIN_DATABASE_URL_asyncpg)  # Подключение к базе по умолчанию
    try:
        db_exists = await conn.fetchval(f"SELECT 1 FROM pg_database WHERE datname = '{settings.DB_NAME}'")
        if not db_exists:
            await conn.execute(f'CREATE DATABASE "{settings.DB_NAME}"')
            logger.info(f"База данных '{settings.DB_NAME}' создана.")
        else:
            logger.warning(f"База данных '{settings.DB_NAME}' уже существует.")
    finally:
        await conn.close()


async def init_db():
    # инициализация БД
    await create_database_if_not_exists()

    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info('Таблицы успешно созданы')
    except Exception as e:
        logger.error(e)
