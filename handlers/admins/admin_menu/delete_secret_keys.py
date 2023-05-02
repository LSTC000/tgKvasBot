from loader import dp, bot

from data.callbacks import DELETE_SECRET_KEYS_DATA

from data.messages import (
    ADMIN_MENU_MESSAGE,
    ENTER_COUNT_DELETE_SECRET_KEYS_MESSAGE,
    COUNT_ERROR_DELETE_SECRET_KEYS_MESSAGE,
    ERROR_DELETE_SECRET_KEYS_MESSAGE,
    SUCCESSFULLY_DELETE_SECRET_KEYS_MESSAGE
)

from keyboards import admin_menu_ikb

from functions import reload_ikb, get_secret_keys_from_cache, delete_available_secret_key_from_cache

from states import AdminMenuStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(lambda c: c.data == DELETE_SECRET_KEYS_DATA, state=AdminMenuStatesGroup.admin_menu)
async def enter_count_delete_secret_keys(callback: types.CallbackQuery) -> None:
    # Спрашиваем количество удаляемых ключей.
    await bot.send_message(chat_id=callback.from_user.id, text=ENTER_COUNT_DELETE_SECRET_KEYS_MESSAGE)

    await AdminMenuStatesGroup.delete_secret_keys.set()


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=AdminMenuStatesGroup.delete_secret_keys)
async def delete_secret_keys(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    try:
        count_delete_secret_keys = int(message.text)

        # Проверяем получили ли мы число большее 0.
        if count_delete_secret_keys > 0:
            # Достаём из БД доступные для удаления ключи.
            secret_keys = await get_secret_keys_from_cache()
            count_secret_keys = len(secret_keys)

            # Если есть доступные ключи ты выводим их пользователю.
            if secret_keys and count_secret_keys >= count_delete_secret_keys:
                for secret_key in secret_keys[:count_delete_secret_keys]:
                    await delete_available_secret_key_from_cache(secret_key)

                await bot.send_message(
                    chat_id=user_id,
                    text=SUCCESSFULLY_DELETE_SECRET_KEYS_MESSAGE.format(count_delete_secret_keys)
                )
            else:
                await bot.send_message(
                    chat_id=user_id,
                    text=COUNT_ERROR_DELETE_SECRET_KEYS_MESSAGE.format(count_delete_secret_keys, count_secret_keys)
                )
        else:
            await bot.send_message(chat_id=user_id, text=ERROR_DELETE_SECRET_KEYS_MESSAGE)
    except ValueError:
        await bot.send_message(chat_id=user_id, text=ERROR_DELETE_SECRET_KEYS_MESSAGE)

    # Вызываем меню администратора.
    await reload_ikb(user_id=user_id, text=ADMIN_MENU_MESSAGE, new_ikb=admin_menu_ikb, state=state)

    await AdminMenuStatesGroup.admin_menu.set()

