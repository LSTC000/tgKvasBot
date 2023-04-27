from loader import dp, buyer_info_cache

from data.callbacks import START_COMMAND_DATA

from data.messages import MAIN_MENU_MESSAGE, FIND_NEAREST_SELLER_MESSAGE, BUYER_REGISTER_MENU_MESSAGE

from data.redis import CITY_REGISTER_REDIS_KEY, BRAND_REGISTER_REDIS_KEY, IKB_PAGE_REDIS_KEY, NEAREST_SELLERS_REDIS_KEY

from keyboards import main_menu_ikb, buyer_register_menu_ikb, buyer_find_nearest_seller_menu_rkb

from functions import is_buyer, reload_ikb, reload_rkb, redis_clear

from states import MainMenuStatesGroup, BuyerRegisterMenuStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.message_handler(commands=['menu'], state='*')
async def menu_command(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    if user_id in buyer_info_cache or await is_buyer(user_id):
        # Удаляем лишние данные из redis, если они есть.
        await redis_clear(state)

        # Вызываем главное меню.
        await reload_ikb(user_id=user_id, text=MAIN_MENU_MESSAGE, new_ikb=main_menu_ikb, state=state)
        await reload_rkb(
            user_id=user_id,
            text=FIND_NEAREST_SELLER_MESSAGE,
            new_rkb=buyer_find_nearest_seller_menu_rkb,
            state=state
        )

        await MainMenuStatesGroup.main_menu.set()
    else:
        # Определяем в redis город и бренд для регистрации.
        async with state.proxy() as data:
            data[CITY_REGISTER_REDIS_KEY] = None
            data[BRAND_REGISTER_REDIS_KEY] = None

        # Вызываем меню регистрации покупателя.
        await reload_ikb(
            user_id=user_id,
            text=BUYER_REGISTER_MENU_MESSAGE,
            new_ikb=buyer_register_menu_ikb,
            state=state
        )

        await BuyerRegisterMenuStatesGroup.register_menu.set()


@dp.callback_query_handler(lambda c: c.data == START_COMMAND_DATA, state='*')
async def callback_menu_command(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    if user_id in buyer_info_cache or await is_buyer(user_id):
        # Удаляем лишние данные из redis, если они есть.
        await redis_clear(state)
        
        # Вызываем главное меню.
        await reload_ikb(user_id=user_id, text=MAIN_MENU_MESSAGE, new_ikb=main_menu_ikb, state=state)
        await reload_rkb(
            user_id=user_id,
            text=FIND_NEAREST_SELLER_MESSAGE,
            new_rkb=buyer_find_nearest_seller_menu_rkb,
            state=state
        )

        await MainMenuStatesGroup.main_menu.set()
    else:
        # Определяем в redis город и бренд для регистрации.
        async with state.proxy() as data:
            data[CITY_REGISTER_REDIS_KEY] = None
            data[BRAND_REGISTER_REDIS_KEY] = None

        # Вызываем меню регистрации покупателя.
        await reload_ikb(user_id=user_id, text=BUYER_REGISTER_MENU_MESSAGE, new_ikb=buyer_register_menu_ikb, state=state)

        await BuyerRegisterMenuStatesGroup.register_menu.set()
