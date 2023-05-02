from loader import dp, bot

from data.callbacks import COUNT_SECRET_KEYS_DATA

from data.messages import ADMIN_MENU_MESSAGE, COUNT_SECRET_KEYS_MESSAGE

from keyboards import admin_menu_ikb

from functions import reload_ikb, get_secret_keys_from_cache

from states import AdminMenuStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(lambda c: c.data == COUNT_SECRET_KEYS_DATA, state=AdminMenuStatesGroup.admin_menu)
async def count_secret_keys(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Достаём из БД доступные для использования ключи.
    secret_keys = await get_secret_keys_from_cache()

    # Показываем количество доступных ключей.
    await bot.send_message(chat_id=user_id, text=COUNT_SECRET_KEYS_MESSAGE.format(len(secret_keys)))

    # Вызываем меню администратора.
    await reload_ikb(user_id=user_id, text=ADMIN_MENU_MESSAGE, new_ikb=admin_menu_ikb, state=state)
