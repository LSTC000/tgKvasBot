import logging

from loader import dp, bot, logger

from data.config import SKIP_UPDATES

from data.messages import ALERT_STARTUP_MESSAGE, ALERT_SHUTDOWN_MESSAGE

from handlers import (
    register_users_cancels_menu,
    register_users_commands,
    register_admins_commands,
    register_admin_menu,
    set_default_commands,
    register_buyer_register_menu,
    register_seller_register_menu,
    register_main_menu,
    register_seller_menu,
    register_buyer_settings_menu,
    register_seller_settings_menu
)

from database import startup_setup, shutdown_setup, get_alerts, delete_buyer_info

from aiogram import Dispatcher
from aiogram.utils import executor
from aiogram.utils.exceptions import (
    BotBlocked,
    ChatNotFound,
    UserDeactivated,
    MigrateToChat,
    Unauthorized,
    BadRequest,
    RetryAfter
)


def register_all_handlers(dispatcher: Dispatcher):
    register_main_menu(dispatcher)
    register_seller_menu(dispatcher)
    register_admin_menu(dispatcher)
    register_buyer_settings_menu(dispatcher)
    register_buyer_register_menu(dispatcher)
    register_seller_settings_menu(dispatcher)
    register_seller_register_menu(dispatcher)
    register_users_cancels_menu(dispatcher)
    register_users_commands(dispatcher)
    register_admins_commands(dispatcher)


async def on_startup(dispatcher: Dispatcher):
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
    )

    logger.info('Setup PostgreSQL connection')
    await startup_setup()

    logger.info('Set all default commands')
    await set_default_commands(bot)

    logger.info('Register all handlers')
    register_all_handlers(dispatcher)

    logger.info('Bot starting users alert')
    users = await get_alerts()
    for user in users:
        user = user[0]
        try:
            await bot.send_message(chat_id=user, text=ALERT_STARTUP_MESSAGE, disable_notification=True)
        except (BotBlocked, ChatNotFound, UserDeactivated, MigrateToChat, Unauthorized, BadRequest, RetryAfter):
            await delete_buyer_info(buyer_id=user)


async def on_shutdown(dispatcher: Dispatcher):
    logger.info('Bot stopped users alert')
    users = await get_alerts()
    for user in users:
        user = user[0]
        try:
            await bot.send_message(chat_id=user, text=ALERT_SHUTDOWN_MESSAGE, disable_notification=True)
        except (BotBlocked, ChatNotFound, UserDeactivated, MigrateToChat, Unauthorized, BadRequest, RetryAfter):
            await delete_buyer_info(buyer_id=user)

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
