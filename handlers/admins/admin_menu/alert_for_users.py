from loader import dp, bot

from data.callbacks import ALERT_FOR_USERS_DATA

from data.messages import (
    ADMIN_MENU_MESSAGE,
    ALERT_FOR_USERS_MESSAGE,
    ERROR_ALERT_FOR_USERS_MESSAGE,
    SUCCESSFULLY_ALERT_FOR_USERS_MESSAGE
)

from database import get_alerts

from keyboards import admin_menu_ikb

from functions import reload_ikb

from states import AdminMenuStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import BotBlocked


@dp.callback_query_handler(lambda c: c.data == ALERT_FOR_USERS_DATA, state=AdminMenuStatesGroup.admin_menu)
async def enter_alert_for_users(callback: types.CallbackQuery) -> None:
    # Просим, чтобы админ ввёл объявление.
    await bot.send_message(chat_id=callback.from_user.id, text=ALERT_FOR_USERS_MESSAGE)

    await AdminMenuStatesGroup.alert_for_users.set()


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=AdminMenuStatesGroup.alert_for_users)
async def alert_for_users(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    text = message.text

    # Проверяем пустое ли сообщение или нет.
    if text:
        users = await get_alerts()
        for user in users:
            try:
                await bot.send_message(chat_id=user[0], text=text, disable_notification=True)
            except BotBlocked:
                pass
        await bot.send_message(chat_id=user_id, text=SUCCESSFULLY_ALERT_FOR_USERS_MESSAGE)
    else:
        await bot.send_message(chat_id=user_id, text=ERROR_ALERT_FOR_USERS_MESSAGE)

    # Вызываем меню администратора.
    await reload_ikb(user_id=user_id, text=ADMIN_MENU_MESSAGE, new_ikb=admin_menu_ikb, state=state)

    await AdminMenuStatesGroup.admin_menu.set()

