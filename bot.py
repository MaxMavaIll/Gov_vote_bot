import asyncio
from distutils.command.config import config
import logging

from aiogram import Bot, Dispatcher, types
from tgbot.hendler.private.users.router import user_router
from tgbot.config import load_config

logger = logging.getLogger(__name__)




async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    config = load_config(".env")
    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher()
    dp['config'] = config
    
    for router in [
        # admin_router,
        # checker_router,
        user_router,
    ]:
        dp.include_router(router)
    
    
    
    await dp.start_polling(bot)




if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('I was stopped')
