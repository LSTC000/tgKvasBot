from loader import dp, seller_info_cache

from data.callbacks import SELLER_MENU_DATA

from data.messages import SELLER_MENU_MESSAGE, SELLER_REGISTER_MENU_MESSAGE, SELLER_UPDATE_GEODATA_MESSAGE

from data.redis import CITY_REGISTER_REDIS_KEY, BRAND_REGISTER_REDIS_KEY

from keyboards import seller_menu_ikb, seller_register_menu_ikb, seller_update_geodata_menu_rkb

from functions import is_seller, reload_ikb, reload_rkb, get_seller_menu_ikb_params

from states import MainMenuStatesGroup, SellerRegisterMenuStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(lambda c: c.data == SELLER_MENU_DATA, state=MainMenuStatesGroup.main_menu)
async def seller_menu(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    if user_id in seller_info_cache or await is_seller(user_id):
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
    else:
        # Определяем в redis город и бренд для регистрации.
        async with state.proxy() as data:
            data[CITY_REGISTER_REDIS_KEY] = None
            data[BRAND_REGISTER_REDIS_KEY] = None

        # Вызываем меню регистрации продавца.
        await reload_ikb(
            user_id=user_id,
            text=SELLER_REGISTER_MENU_MESSAGE,
            new_ikb=seller_register_menu_ikb,
            state=state
        )

        await SellerRegisterMenuStatesGroup.register_menu.set()
