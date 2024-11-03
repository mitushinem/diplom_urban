import asyncio
from config.config import logger
from loader import dp, bot
from handlers.default_heandlers.help import router_help
from handlers.default_heandlers.start import router_start
from handlers.default_heandlers.cancel import router_cancel
from handlers.custom_heandlers.lowprice import router_lowprice
from handlers.custom_heandlers.highprice import router_highprice
from handlers.custom_heandlers.bestdeal import router_bestdeal


async def main():
    dp.include_router(router_help)
    dp.include_router(router_start)
    dp.include_router(router_cancel)
    dp.include_router(router_lowprice)
    dp.include_router(router_highprice)
    dp.include_router(router_bestdeal)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
        logger.info('Бот запущен')
    except KeyboardInterrupt:
        logger.info('Бот выключен')
    except Exception as e:
        logger.error(e)

# Cause exception while process update id=110549430 by bot id=2031605608
# TelegramNetworkError: HTTP Client says - ClientConnectorError: Cannot connect to host api.telegram.org:443 ssl:default [None]
# Traceback (most recent call last):