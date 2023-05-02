from loader import dp, bot

from data.callbacks import SHOW_SECRET_KEYS_DATA

from data.messages import (
    ADMIN_MENU_MESSAGE,
    ENTER_COUNT_SHOW_SECRET_KEYS_MESSAGE,
    COUNT_ERROR_SHOW_SECRET_KEYS_MESSAGE,
    ERROR_SHOW_SECRET_KEYS_MESSAGE
)

from keyboards import admin_menu_ikb

from functions import reload_ikb, get_secret_keys_from_cache

from states import AdminMenuStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(lambda c: c.data == SHOW_SECRET_KEYS_DATA, state=AdminMenuStatesGroup.admin_menu)
async def enter_count_show_secret_keys(callback: types.CallbackQuery) -> None:
    # Спрашиваем количество показываемых ключей.
    await bot.send_message(chat_id=callback.from_user.id, text=ENTER_COUNT_SHOW_SECRET_KEYS_MESSAGE)

    await AdminMenuStatesGroup.show_secret_keys.set()


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=AdminMenuStatesGroup.show_secret_keys)
async def show_secret_keys(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    try:
        count_show_secret_keys = int(message.text)

        # Проверяем получили ли мы число большее 0.
        if count_show_secret_keys > 0:
            # Достаём из БД доступные для использования ключи.
            secret_keys = await get_secret_keys_from_cache()
            count_secret_keys = len(secret_keys)

            # Если есть доступные ключи и их количество >= количества запрашиваемых ключей, то выводим их пользователю.
            if secret_keys and count_secret_keys >= count_show_secret_keys:
                report = ''

                for i, secret_key in enumerate(secret_keys[:count_show_secret_keys]):
                    report += f'{i + 1}: <b>{secret_key}</b>\n\n'

                await bot.send_message(chat_id=user_id, text=report)
            else:
                await bot.send_message(
                    chat_id=user_id,
                    text=COUNT_ERROR_SHOW_SECRET_KEYS_MESSAGE.format(count_show_secret_keys, count_secret_keys)
                )
        else:
            await bot.send_message(chat_id=user_id, text=ERROR_SHOW_SECRET_KEYS_MESSAGE)
    except ValueError:
        await bot.send_message(chat_id=user_id, text=ERROR_SHOW_SECRET_KEYS_MESSAGE)

    # Вызываем меню администратора.
    await reload_ikb(user_id=user_id, text=ADMIN_MENU_MESSAGE, new_ikb=admin_menu_ikb, state=state)

    await AdminMenuStatesGroup.admin_menu.set()
