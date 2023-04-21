from loader import dp, bot

from data.redis import LAST_IKB_REDIS_KEY, CITY_REGISTER_REDIS_KEY, BRAND_REGISTER_REDIS_KEY

from data.callbacks import CONFIRM_SELLER_REGISTER_DATA

from data.messages import (
    SELLER_MENU_MESSAGES,
    SELLER_REGISTER_MENU_MESSAGE,
    SELLER_SUCCESSFULLY_REGISTER_MESSAGE,
    SELLER_UNSUCCESSFULLY_REGISTER_MESSAGE,
    SELLER_ENTER_REGISTER_CODE_MESSAGE,
    SELLER_UNSUCCESSFULLY_ENTER_REGISTER_CODE_MESSAGE
)

from database import add_seller, add_seller_info, add_seller_address

from functions import reload_ikb, get_seller_menu_ikb_params

from keyboards import seller_menu_ikb, seller_register_menu_ikb

from states import MainMenuStatesGroup, SellerRegisterMenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound


@dp.callback_query_handler(
    lambda c: c.data == CONFIRM_SELLER_REGISTER_DATA,
    state=SellerRegisterMenuStatesGroup.register_menu
)
async def seller_confirm_register(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Достаём из redis выбранные пользователем город и бренд.
    async with state.proxy() as data:
        city = data[CITY_REGISTER_REDIS_KEY]
        brand = data[BRAND_REGISTER_REDIS_KEY]

    # Проверяем выбрал пользователь город и бренд или нет. От этого будет зависить разрешение на регистрацию покупателю.
    if city is not None and brand is not None:
        async with state.proxy() as data:
            if LAST_IKB_REDIS_KEY in data:
                try:
                    await bot.delete_message(chat_id=user_id, message_id=data[LAST_IKB_REDIS_KEY])
                except MessageToDeleteNotFound:
                    pass

        # Отправляем пользователю сообщение о необходимсоти ввести секретный код для успешной регистрации.
        await bot.send_message(chat_id=user_id, text=SELLER_ENTER_REGISTER_CODE_MESSAGE)

        await SellerRegisterMenuStatesGroup.register_code.set()
    else:
        # Сообщаем пользователю о том, что для регистрации нужно выбрать город и бренд.
        await bot.send_message(chat_id=user_id, text=SELLER_UNSUCCESSFULLY_REGISTER_MESSAGE)

        # Вызываем меню регистрации.
        await reload_ikb(
            user_id=user_id,
            text=SELLER_REGISTER_MENU_MESSAGE,
            new_ikb=seller_register_menu_ikb,
            state=state
        )

        await SellerRegisterMenuStatesGroup.register_menu.set()


@dp.message_handler(content_types=['text'], state=SellerRegisterMenuStatesGroup.register_code)
async def enter_seller_register_code(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    # Достаём из redis выбранные пользователем город и бренд.
    async with state.proxy() as data:
        city = data[CITY_REGISTER_REDIS_KEY]
        brand = data[BRAND_REGISTER_REDIS_KEY]

    if message.text == '12345':
        # Добавляем в БД данные о продавце.
        await add_seller(seller_id=user_id)
        await add_seller_info(seller_id=user_id)
        await add_seller_address(seller_id=user_id, city=city, brand=brand)

        # Удаляем из redis выбранные пользователем город и бренд.
        async with state.proxy() as data:
            data.pop(CITY_REGISTER_REDIS_KEY)
            data.pop(BRAND_REGISTER_REDIS_KEY)

        # Сообщаем покупателю о успешной регистрации.
        await bot.send_message(chat_id=user_id, text=SELLER_SUCCESSFULLY_REGISTER_MESSAGE)

        # Вызываем меню продавца.
        await reload_ikb(
            user_id=user_id,
            text=SELLER_MENU_MESSAGES,
            new_ikb=seller_menu_ikb,
            state=state,
            ikb_params=await get_seller_menu_ikb_params(user_id)
        )

        await MainMenuStatesGroup.seller_menu.set()
    else:
        # Сообщаем пользователю о том, что он ввёл неверный код для регистрации.
        await bot.send_message(chat_id=user_id, text=SELLER_UNSUCCESSFULLY_ENTER_REGISTER_CODE_MESSAGE)

        # Вызываем меню регистрации.
        await reload_ikb(
            user_id=user_id,
            text=SELLER_REGISTER_MENU_MESSAGE,
            new_ikb=seller_register_menu_ikb,
            state=state
        )

        await SellerRegisterMenuStatesGroup.register_menu.set()
