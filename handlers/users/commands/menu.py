from loader import dp, buyer_cache

from data.messages import MENU_MESSAGE, BUYER_REGISTER_MESSAGE

from data.redis import CITY_REGISTER_REDIS_KEY, BRAND_REGISTER_REDIS_KEY

from keyboards import main_menu_ikb, buyer_register_menu_ikb

from functions import is_buyer, reload_ikb

from states import MainMenuStatesGroup, BuyerRegisterMenuStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.message_handler(commands=['menu'], state='*')
async def menu_command(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    if user_id in buyer_cache:
        async with state.proxy() as data:
            # Очищаем все данные пользователя в redis.
            data.clear()

        # Вызываем главное меню.
        await reload_ikb(user_id=user_id, text=MENU_MESSAGE, new_ikb=main_menu_ikb, state=state)

        await MainMenuStatesGroup.main_menu.set()
    elif await is_buyer(user_id):
        buyer_cache[user_id] = None

        async with state.proxy() as data:
            # Очищаем все данные пользователя в redis.
            data.clear()

        # Вызываем главное меню.
        await reload_ikb(user_id=user_id, text=MENU_MESSAGE, new_ikb=main_menu_ikb, state=state)

        await MainMenuStatesGroup.main_menu.set()
    else:
        # Определяем в redis город и бренд для регистрации.
        async with state.proxy() as data:
            data[CITY_REGISTER_REDIS_KEY] = None
            data[BRAND_REGISTER_REDIS_KEY] = None

        # Вызываем меню регистрации покупателя.
        await reload_ikb(user_id=user_id, text=BUYER_REGISTER_MESSAGE, new_ikb=buyer_register_menu_ikb, state=state)

        await BuyerRegisterMenuStatesGroup.register_menu.set()
