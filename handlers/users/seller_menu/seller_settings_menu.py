from loader import dp

from data.callbacks import SETTINGS_SELLER_MENU_DATA

from data.messages import SELLER_SETTINGS_MENU_MESSAGE

from functions import reload_ikb

from keyboards import seller_settings_menu_ikb

from states import MainMenuStatesGroup, SellerMenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda c: c.data == SETTINGS_SELLER_MENU_DATA, state=MainMenuStatesGroup.seller_menu)
async def seller_settings_menu(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Вызываем меню настроек продавца.
    await reload_ikb(
        user_id=user_id,
        text=SELLER_SETTINGS_MENU_MESSAGE,
        new_ikb=seller_settings_menu_ikb,
        state=state
    )

    await SellerMenuStatesGroup.settings_menu.set()
