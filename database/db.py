from datetime import datetime, timedelta
from config.config import logger
from sqlalchemy import select, and_, delete
from database.models import User, History, async_session


async def set_user(telegram_id, name):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == telegram_id))

        if not user:
            session.add(User(telegram_id=telegram_id, name=name))
            await session.commit()
            logger.info(f'Пользователь с ID {telegram_id} создан')


async def add_record(telegram_id, command, hotels, city):
    """
    Добавление записи в БД
    """
    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.telegram_id == telegram_id))

            session.add(
                History(
                    command=command,
                    hotels=hotels,
                    user_id=user.user_id,
                    city=city)
            )

            await session.commit()
        except Exception as e:
            logger.error(e)


async def select_all_record(telegram_id, ):
    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.telegram_id == telegram_id))

            if not user:
                return None

            records = await session.scalars(select(History).where(History.user_id == user.user_id))

            if records:
                return records.all()
            return None
        except Exception as e:
            logger.error(e)


async def select_all_record_for_days(telegram_id: int, days: int = 0):
    if days == 0:
        lo = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        lo = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days)
    hi = datetime.now().replace(microsecond=0)

    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.telegram_id == telegram_id))

            if not user:
                return None

            records = await session.scalars(select(History).where(and_(History.user_id == user.user_id,
                                                                       History.created_at.between(lo, hi))))
            if records:
                return records.all()
            return None

        except Exception as e:
            logger.error(e)


async def delete_all_record(telegram_id: int) -> None:
    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.telegram_id == telegram_id))

            if user:
                await session.execute(delete(History).where(History.user_id == user.user_id))
                await session.commit()

        except Exception as e:
            logger.error(e)
