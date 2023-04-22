from loader import dp

from data.callbacks import CANCEL_TO_SELLER_MENU_DATA

from data.messages import SELLER_MENU_MESSAGE, SELLER_UPDATE_GEODATA_MESSAGE

from functions import reload_ikb, reload_rkb, get_seller_menu_ikb_params

from keyboards import seller_menu_ikb, seller_update_geodata_menu_rkb

from states import MainMenuStatesGroup, SellerMenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda c: c.data == CANCEL_TO_SELLER_MENU_DATA, state=SellerMenuStatesGroup.settings_menu)
async def cancel_to_seller_menu(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Вызываем меню продавца.
    await reload_ikb(
        user_id=user_id,
        text=SELLER_MENU_MESSAGE,
        new_ikb=seller_menu_ikb,
        state=state,
        ikb_params=await get_seller_menu_ikb_params(user_id)
    )
    await reload_rkb(
        user_id=user_id,
        text=SELLER_UPDATE_GEODATA_MESSAGE,
        new_rkb=seller_update_geodata_menu_rkb,
        state=state
    )

    await MainMenuStatesGroup.seller_menu.set()
