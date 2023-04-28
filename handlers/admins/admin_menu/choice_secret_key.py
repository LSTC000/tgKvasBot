from loader import dp, bot

from data.callbacks import SHOW_AVAILABLE_SECRET_KEYS_DATA, CANCEL_TO_LAST_MENU_DATA

from data.messages import ADMIN_MENU_MESSAGE, CHOICE_SECRET_KEY_MESSAGE, SUCCESSFULLY_CHOICE_SECRET_KEY_MESSAGE

from keyboards import choice_secret_key_menu_ikb, admin_menu_ikb

from functions import reload_ikb, get_secret_keys_from_cache

from states import AdminMenuStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(lambda c: c.data == SHOW_AVAILABLE_SECRET_KEYS_DATA, state=AdminMenuStatesGroup.admin_menu)
async def show_available_secret_keys(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Достаём из БД доступные для использования ключи.
    secret_keys = await get_secret_keys_from_cache()

    # Вызываем меню для выбора секретного ключа.
    await reload_ikb(
        user_id=user_id,
        text=CHOICE_SECRET_KEY_MESSAGE,
        new_ikb=choice_secret_key_menu_ikb,
        state=state,
        ikb_params={'secret_keys': secret_keys}
    )

    await AdminMenuStatesGroup.choice_secret_key.set()


@dp.callback_query_handler(state=AdminMenuStatesGroup.choice_secret_key)
async def choice_secret_key(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id
    secret_key = callback.data

    # Проверяем выбрал ли админстратор какой-либо из секретных ключей.
    if secret_key != CANCEL_TO_LAST_MENU_DATA:
        # Отправляем администратору выбранный ключ.
        await bot.send_message(chat_id=user_id, text=SUCCESSFULLY_CHOICE_SECRET_KEY_MESSAGE.format(secret_key))

    # Вызываем меню администратора.
    await reload_ikb(user_id=user_id, text=ADMIN_MENU_MESSAGE, new_ikb=admin_menu_ikb, state=state)

    await AdminMenuStatesGroup.admin_menu.set()
