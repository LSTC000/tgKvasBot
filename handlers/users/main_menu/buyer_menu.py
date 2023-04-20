from loader import dp

from data.callbacks import BUYER_MENU_DATA

from data.messages import BUYER_SETTINGS_MENU_MESSAGE

from functions import reload_ikb

from keyboards import buyer_menu_ikb

from states import MainMenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda c: c.data == BUYER_MENU_DATA, state=MainMenuStatesGroup.main_menu)
async def buyer_menu(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Вызываем меню покупателя.
    await reload_ikb(user_id=user_id, text=BUYER_SETTINGS_MENU_MESSAGE, new_ikb=buyer_menu_ikb, state=state)

    await MainMenuStatesGroup.buyer_menu.set()
