from loader import dp, bot

from data.redis import CITY_REGISTER_REDIS_KEY, BRAND_REGISTER_REDIS_KEY

from data.callbacks import CONFIRM_BUYER_REGISTER_DATA

from data.messages import (
    MENU_MESSAGE,
    BUYER_REGISTER_MENU_MESSAGE,
    BUYER_SUCCESSFULLY_REGISTER_MESSAGE,
    BUYER_UNSUCCESSFULLY_REGISTER_MESSAGE
)

from database import add_alert, add_buyer

from functions import reload_ikb

from keyboards import main_menu_ikb, buyer_register_menu_ikb

from states import MainMenuStatesGroup, BuyerRegisterMenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(
    lambda c: c.data == CONFIRM_BUYER_REGISTER_DATA,
    state=BuyerRegisterMenuStatesGroup.register_menu
)
async def buyer_confirm_register(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Достаём из redis выбранные пользователем город и бренд.
    async with state.proxy() as data:
        city = data[CITY_REGISTER_REDIS_KEY]
        brand = data[BRAND_REGISTER_REDIS_KEY]

    # Проверяем выбрал пользователь город или нет. От этого будет зависить разрешение на регистрацию покупателю.
    if city is not None:
        # Добавляем в БД данные о покупателе и в список тех, кто будет получать уведомления.
        await add_buyer(buyer_id=user_id, city=city, brand=brand)
        await add_alert(user_id=user_id)

        # Сообщаем покупателю о успешной регистрации.
        await bot.send_message(chat_id=user_id, text=BUYER_SUCCESSFULLY_REGISTER_MESSAGE)

        # Удаляем из redis выбранные пользователем город и бренд.
        async with state.proxy() as data:
            data.pop(CITY_REGISTER_REDIS_KEY)
            data.pop(BRAND_REGISTER_REDIS_KEY)

        # Вызываем главное меню.
        await reload_ikb(user_id=user_id, text=MENU_MESSAGE, new_ikb=main_menu_ikb, state=state)

        await MainMenuStatesGroup.main_menu.set()
    else:
        # Сообщаем пользователю о том, что для регистрации нужно выбрать город.
        await bot.send_message(chat_id=user_id, text=BUYER_UNSUCCESSFULLY_REGISTER_MESSAGE)

        # Вызываем меню регистрации.
        await reload_ikb(
            user_id=user_id,
            text=BUYER_REGISTER_MENU_MESSAGE,
            new_ikb=buyer_register_menu_ikb,
            state=state
        )

        await BuyerRegisterMenuStatesGroup.register_menu.set()
