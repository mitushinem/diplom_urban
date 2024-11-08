import asyncio
from config.config import logger
from loader import dp, bot
from handlers.default_heandlers.help import router_help
from handlers.default_heandlers.start import router_start
from handlers.default_heandlers.cancel import router_cancel
from handlers.custom_heandlers.lowprice import router_lowprice
from handlers.custom_heandlers.highprice import router_highprice
from handlers.custom_heandlers.bestdeal import router_bestdeal
from handlers.custom_heandlers.history import router_history
from database.models import init_db


async def main():
    await init_db()

    dp.include_router(router_help)
    dp.include_router(router_start)
    dp.include_router(router_cancel)
    dp.include_router(router_lowprice)
    dp.include_router(router_highprice)
    dp.include_router(router_bestdeal)
    dp.include_router(router_history)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main(), debug=True)
        logger.info('Бот запущен')
    except KeyboardInterrupt:
        logger.info('Бот выключен')
    except Exception as e:
        logger.error(e)
