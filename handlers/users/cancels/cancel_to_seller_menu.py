from loader import dp

from data.callbacks import CANCEL_TO_MAIN_MENU_DATA

from data.messages import SELLER_MENU_MESSAGES

from functions import reload_ikb, get_seller_menu_ikb_params

from keyboards import seller_menu_ikb

from states import MainMenuStatesGroup, SellerMenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda c: c.data == CANCEL_TO_MAIN_MENU_DATA, state=SellerMenuStatesGroup.settings_menu)
async def cancel_to_seller_menu(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Вызываем меню продавца.
    await reload_ikb(
        user_id=user_id,
        text=SELLER_MENU_MESSAGES,
        new_ikb=seller_menu_ikb,
        state=state,
        ikb_params=await get_seller_menu_ikb_params(user_id)
    )

    await MainMenuStatesGroup.seller_menu.set()
