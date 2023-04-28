from loader import dp

from data.config import ADMINS

from data.messages import ADMIN_MENU_MESSAGE

from keyboards import admin_menu_ikb

from functions import reload_ikb, redis_clear

from states import AdminMenuStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.message_handler(commands=['admin'], state='*')
async def admin_command(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    if user_id in ADMINS:
        # Удаляем лишние данные из redis, если они есть.
        await redis_clear(state)

        # Вызываем меню администратора.
        await reload_ikb(user_id=user_id, text=ADMIN_MENU_MESSAGE, new_ikb=admin_menu_ikb, state=state)

        await AdminMenuStatesGroup.admin_menu.set()
