from loader import dp, bot

from data.callbacks import ALERT_FOR_USERS_DATA, CONFIRM_ALERT_FOR_USERS_DATA, CANCEL_ALERT_FOR_USERS_DATA

from data.redis import ALERT_FOR_USERS_REDIS_KEY

from data.messages import (
    ADMIN_MENU_MESSAGE,
    ALERT_FOR_USERS_MESSAGE,
    CONFIRM_ALERT_FOR_USERS_MESSAGE,
    ERROR_ALERT_FOR_USERS_MESSAGE,
    SUCCESSFULLY_ALERT_FOR_USERS_MESSAGE
)

from database import get_alerts, delete_buyer_info

from keyboards import admin_menu_ikb, confirm_alert_for_users_menu_ikb

from functions import reload_ikb

from states import AdminMenuStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import (
    BotBlocked,
    ChatNotFound,
    UserDeactivated,
    MigrateToChat,
    Unauthorized,
    BadRequest,
    RetryAfter
)


@dp.callback_query_handler(lambda c: c.data == ALERT_FOR_USERS_DATA, state=AdminMenuStatesGroup.admin_menu)
async def enter_alert_for_users(callback: types.CallbackQuery) -> None:
    # Просим, чтобы админ ввёл уведомление.
    await bot.send_message(chat_id=callback.from_user.id, text=ALERT_FOR_USERS_MESSAGE)

    await AdminMenuStatesGroup.alert_for_users.set()


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=AdminMenuStatesGroup.alert_for_users)
async def alert_for_users(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    text = message.text

    # Проверяем пустое ли сообщение или нет.
    if text:
        async with state.proxy() as data:
            data[ALERT_FOR_USERS_REDIS_KEY] = text

        # Вызываем меню подтверждения отправки уведомления.
        await reload_ikb(
            user_id=user_id,
            text=CONFIRM_ALERT_FOR_USERS_MESSAGE.format(text),
            new_ikb=confirm_alert_for_users_menu_ikb,
            state=state
        )

        await AdminMenuStatesGroup.confirm_for_users.set()
    else:
        await bot.send_message(chat_id=user_id, text=ERROR_ALERT_FOR_USERS_MESSAGE)

        # Вызываем меню администратора.
        await reload_ikb(user_id=user_id, text=ADMIN_MENU_MESSAGE, new_ikb=admin_menu_ikb, state=state)

        await AdminMenuStatesGroup.admin_menu.set()


@dp.callback_query_handler(
    lambda c: c.data in [CONFIRM_ALERT_FOR_USERS_DATA, CANCEL_ALERT_FOR_USERS_DATA],
    state=AdminMenuStatesGroup.confirm_for_users
)
async def confirm_alert_for_users(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    async with state.proxy() as data:
        text = data[ALERT_FOR_USERS_REDIS_KEY]
        data.pop(ALERT_FOR_USERS_REDIS_KEY)

    # Если админимстратор подтвердил отправку уведомления, то отправляем его.
    if callback.data == CONFIRM_ALERT_FOR_USERS_DATA:
        users = await get_alerts()
        for user in users:
            user = user[0]
            try:
                await bot.send_message(chat_id=user, text=text, disable_notification=True)
            except (BotBlocked, ChatNotFound, UserDeactivated, MigrateToChat, Unauthorized, BadRequest, RetryAfter):
                await delete_buyer_info(buyer_id=user)

        await bot.send_message(chat_id=user_id, text=SUCCESSFULLY_ALERT_FOR_USERS_MESSAGE)

    # Вызываем меню администратора.
    await reload_ikb(user_id=user_id, text=ADMIN_MENU_MESSAGE, new_ikb=admin_menu_ikb, state=state)

    await AdminMenuStatesGroup.admin_menu.set()
