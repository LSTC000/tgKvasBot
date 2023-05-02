from loader import dp, bot

from data.callbacks import CREATE_SECRET_KEY_DATA

from data.messages import (
    ADMIN_MENU_MESSAGE,
    ENTER_COUNT_CREATE_SECRET_KEYS_MESSAGE,
    ERROR_CREATE_SECRET_KEYS_MESSAGE,
    SUCCESSFULLY_CREATE_SECRET_KEYS_MESSAGE
)

from keyboards import admin_menu_ikb

from functions import reload_ikb, add_secret_key_from_cache

from states import AdminMenuStatesGroup

from utils import generate_secret_key

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(lambda c: c.data == CREATE_SECRET_KEY_DATA, state=AdminMenuStatesGroup.admin_menu)
async def enter_count_create_secret_keys(callback: types.CallbackQuery) -> None:
    # Спрашиваем количество создаваемых ключей.
    await bot.send_message(chat_id=callback.from_user.id, text=ENTER_COUNT_CREATE_SECRET_KEYS_MESSAGE)

    await AdminMenuStatesGroup.create_secret_keys.set()


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=AdminMenuStatesGroup.create_secret_keys)
async def create_secret_keys(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    try:
        count_create_secret_keys = int(message.text)

        # Проверяем получили ли мы число большее 0.
        if count_create_secret_keys > 0:
            # Генерируем новый ключ для регистрации продавца и добавляем его в БД и кэш.
            for _ in range(count_create_secret_keys):
                secret_key = generate_secret_key()
                await add_secret_key_from_cache(secret_key)

            # Отправляем сообщение о успешном создании всех ключей.
            await bot.send_message(
                chat_id=user_id,
                text=SUCCESSFULLY_CREATE_SECRET_KEYS_MESSAGE.format(count_create_secret_keys)
            )
        else:
            await bot.send_message(chat_id=user_id, text=ERROR_CREATE_SECRET_KEYS_MESSAGE)
    except ValueError:
        await bot.send_message(chat_id=user_id, text=ERROR_CREATE_SECRET_KEYS_MESSAGE)

    # Вызываем меню администратора.
    await reload_ikb(user_id=user_id, text=ADMIN_MENU_MESSAGE, new_ikb=admin_menu_ikb, state=state)

    await AdminMenuStatesGroup.admin_menu.set()
