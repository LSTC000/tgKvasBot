import logging

from data.config import SKIP_UPDATES

# from data.messages import (
#     ADMIN_STARTUP_MESSAGE,
#     ADMIN_SHUTDOWN_MESSAGE,
#     USERS_STARTUP_MESSAGE,
#     USERS_SHUTDOWN_MESSAGE
# )

from handlers import (
    register_users_commands,
    set_default_commands
)

from loader import dp, bot, logger

from database import startup_setup, shutdown_setup


from aiogram import Bot, Dispatcher
from aiogram.utils import executor


def register_all_handlers(dispatcher: Dispatcher):
    register_users_commands(dispatcher)


# def register_all_middlewares(dispatcher: Dispatcher):
#     dispatcher.setup_middleware(ThrottlingAndDatabaseMiddleware())


async def on_startup(dispatcher: Dispatcher):
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
    )

    logger.info('Setup PostgreSQL connection')
    await startup_setup()

    # logger.info('Register all middlewares')
    # register_all_middlewares(dispatcher)
    #
    logger.info('Set all default commands')
    await set_default_commands(bot)

    logger.info('Register all handlers')
    register_all_handlers(dispatcher)

    # logger.info('Bot starting users alert')
    # users = await select_users()
    # for user in users:
    #     await bot.send_message(chat_id=user[0], text=USERS_STARTUP_MESSAGE)


async def on_shutdown(dispatcher: Dispatcher):
    # logger.info('Bot stopped users alert')
    # users = await select_users()
    # for user in users:
    #     await bot.send_message(chat_id=user[0], text=USERS_SHUTDOWN_MESSAGE)

    logger.info('Closing PostgreSQL connection')
    await shutdown_setup()

    logger.info('Closing storage')
    await dp.storage.close()


if __name__ == '__main__':
    try:
        executor.start_polling(
            dispatcher=dp,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=SKIP_UPDATES
        )
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
        raise

