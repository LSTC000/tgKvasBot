from loader import dp, bot

from data.redis import LAST_IKB_REDIS_KEY, IKB_PAGE_REDIS_KEY, CITY_REGISTER_REDIS_KEY

from data.callbacks import BUYER_CHOICE_CITY_DATA

from data.messages import BUYER_REGISTER_MESSAGE, BUYER_CHOICE_CITY_MESSAGE, BUYER_SAVE_CHOICE_CITY_MESSAGE

from functions import get_cities_from_cache, reload_ikb

from keyboards import buyer_register_menu_ikb

from states import BuyerRegisterMenuStatesGroup

from inline_pickers import InlineCityPicker

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound


@dp.callback_query_handler(
    lambda c: c.data == BUYER_CHOICE_CITY_DATA,
    state=BuyerRegisterMenuStatesGroup.register_menu
)
async def buyer_choice_city(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    async with state.proxy() as data:
        if LAST_IKB_REDIS_KEY in data:
            try:
                await bot.delete_message(chat_id=user_id, message_id=data[LAST_IKB_REDIS_KEY])
            except MessageToDeleteNotFound:
                pass

        # Достаём список доступных городов и запоминаем в redis страницу.
        cities = await get_cities_from_cache()
        data[IKB_PAGE_REDIS_KEY] = 0

        # Вызываем меню выбора города.
        msg = await bot.send_message(
            chat_id=user_id,
            text=BUYER_CHOICE_CITY_MESSAGE,
            reply_markup=await InlineCityPicker().start_citypicker(cities=cities, page=0)
        )

        data[LAST_IKB_REDIS_KEY] = msg.message_id

    await BuyerRegisterMenuStatesGroup.choice_city.set()


@dp.callback_query_handler(state=BuyerRegisterMenuStatesGroup.choice_city)
async def enter_buyer_choice_city(callback: types.CallbackQuery, state: FSMContext) -> None:
    # Достаём список доступных городов.
    cities = await get_cities_from_cache()

    # Принимаем ответ от меню выбора города.
    selected, city = await InlineCityPicker().process_selection(
        cities=cities,
        callback=callback,
        callback_data=callback.data,
        state=state
    )

    # Проверяем получили ли мы город от пользователя.
    if selected:
        user_id = callback.from_user.id

        if city is not None:
            # Добавляем в redis выбранный город и отправляем об этом сообщение.
            async with state.proxy() as data:
                data[CITY_REGISTER_REDIS_KEY] = city
                await bot.send_message(chat_id=user_id, text=BUYER_SAVE_CHOICE_CITY_MESSAGE)

        # Удаляем страницу из redis.
        async with state.proxy() as data:
            data.pop(IKB_PAGE_REDIS_KEY)

        # Вызываем меню регистрации.
        await reload_ikb(user_id=user_id, text=BUYER_REGISTER_MESSAGE, new_ikb=buyer_register_menu_ikb, state=state)

        await BuyerRegisterMenuStatesGroup.register_menu.set()
