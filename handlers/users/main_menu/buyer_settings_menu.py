from loader import dp

from data.callbacks import SETTINGS_MAIN_MENU_DATA

from data.messages import BUYER_SETTINGS_MENU_MESSAGE

from functions import reload_ikb, get_buyer_settings_menu_ikb_params

from keyboards import buyer_settings_menu_ikb

from states import MainMenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda c: c.data == SETTINGS_MAIN_MENU_DATA, state=MainMenuStatesGroup.main_menu)
async def buyer_settings_menu(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Вызываем меню настроек покупателя.
    await reload_ikb(
        user_id=user_id,
        text=BUYER_SETTINGS_MENU_MESSAGE,
        new_ikb=buyer_settings_menu_ikb,
        state=state,
        ikb_params=await get_buyer_settings_menu_ikb_params(user_id)
    )

    await MainMenuStatesGroup.settings_menu.set()
