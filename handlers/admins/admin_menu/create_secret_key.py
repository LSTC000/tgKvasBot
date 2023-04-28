from loader import dp, bot

from data.callbacks import CREATE_SECRET_KEY_DATA

from data.messages import ADMIN_MENU_MESSAGE, SUCCESSFULLY_CREATE_SECRET_KEY_MESSAGE

from keyboards import admin_menu_ikb

from functions import reload_ikb, add_secret_key_from_cache

from states import AdminMenuStatesGroup

from utils import generate_secret_key

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(lambda c: c.data == CREATE_SECRET_KEY_DATA, state=AdminMenuStatesGroup.admin_menu)
async def create_secret_key(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Генерируем новый ключ для регистрации продавца и добавляем его в БД и кэш.
    secret_key = generate_secret_key()
    await add_secret_key_from_cache(secret_key)

    # Отправляем сообщение о успешном создании ключа.
    await bot.send_message(chat_id=user_id, text=SUCCESSFULLY_CREATE_SECRET_KEY_MESSAGE.format(secret_key))

    # Вызываем меню администратора.
    await reload_ikb(user_id=user_id, text=ADMIN_MENU_MESSAGE, new_ikb=admin_menu_ikb, state=state)
