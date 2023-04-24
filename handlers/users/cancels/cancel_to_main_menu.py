from loader import dp

from data.redis import CITY_REGISTER_REDIS_KEY, BRAND_REGISTER_REDIS_KEY

from data.callbacks import CANCEL_TO_MAIN_MENU_DATA

from data.messages import MAIN_MENU_MESSAGE, FIND_NEAREST_SELLER_MESSAGE

from functions import reload_ikb, reload_rkb

from keyboards import main_menu_ikb, buyer_find_nearest_seller_menu_rkb

from states import MainMenuStatesGroup, SellerRegisterMenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(
    lambda c: c.data == CANCEL_TO_MAIN_MENU_DATA,
    state=[
        MainMenuStatesGroup.find_nearest_seller,
        MainMenuStatesGroup.settings_menu,
        MainMenuStatesGroup.seller_menu,
        SellerRegisterMenuStatesGroup.register_menu
    ]
)
async def cancel_to_main_menu(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Удаляем лишние данные из redis, если они есть.
    async with state.proxy() as data:
        if CITY_REGISTER_REDIS_KEY in data:
            data.pop(CITY_REGISTER_REDIS_KEY)

        if BRAND_REGISTER_REDIS_KEY in data:
            data.pop(BRAND_REGISTER_REDIS_KEY)

    # Вызываем главное меню.
    await reload_ikb(user_id=user_id, text=MAIN_MENU_MESSAGE, new_ikb=main_menu_ikb, state=state)
    await reload_rkb(
        user_id=user_id,
        text=FIND_NEAREST_SELLER_MESSAGE,
        new_rkb=buyer_find_nearest_seller_menu_rkb,
        state=state
    )

    await MainMenuStatesGroup.main_menu.set()
