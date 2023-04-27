from loader import dp, bot

from data.redis import LAST_IKB_REDIS_KEY, IKB_PAGE_REDIS_KEY, CITY_REGISTER_REDIS_KEY

from data.callbacks import SELLER_CHOICE_CITY_DATA

from data.messages import SELLER_REGISTER_MENU_MESSAGE, SELLER_CHOICE_CITY_MESSAGE, SELLER_SAVE_CHOICE_CITY_MESSAGE

from functions import get_cities_from_cache, reload_ikb

from keyboards import seller_register_menu_ikb

from states import SellerRegisterMenuStatesGroup

from inline_pickers import InlineCityPicker

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound, MessageCantBeDeleted


@dp.callback_query_handler(
    lambda c: c.data == SELLER_CHOICE_CITY_DATA,
    state=SellerRegisterMenuStatesGroup.register_menu
)
async def seller_choice_city(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    async with state.proxy() as data:
        if LAST_IKB_REDIS_KEY in data:
            try:
                await bot.delete_message(chat_id=user_id, message_id=data[LAST_IKB_REDIS_KEY])
            except (MessageToDeleteNotFound, MessageCantBeDeleted):
                pass

        # Достаём список доступных городов и запоминаем в redis страницу.
        cities = await get_cities_from_cache()
        data[IKB_PAGE_REDIS_KEY] = 0

        # Вызываем меню выбора города.
        msg = await bot.send_message(
            chat_id=user_id,
            text=SELLER_CHOICE_CITY_MESSAGE,
            reply_markup=await InlineCityPicker().start_city_picker(cities=cities, page=0)
        )

        data[LAST_IKB_REDIS_KEY] = msg.message_id

    await SellerRegisterMenuStatesGroup.choice_city.set()


@dp.callback_query_handler(state=SellerRegisterMenuStatesGroup.choice_city)
async def enter_seller_choice_city(callback: types.CallbackQuery, state: FSMContext) -> None:
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
                await bot.send_message(chat_id=user_id, text=SELLER_SAVE_CHOICE_CITY_MESSAGE)

        # Удаляем страницу из redis.
        async with state.proxy() as data:
            data.pop(IKB_PAGE_REDIS_KEY)

        # Вызываем меню регистрации.
        await reload_ikb(
            user_id=user_id,
            text=SELLER_REGISTER_MENU_MESSAGE,
            new_ikb=seller_register_menu_ikb,
            state=state
        )

        await SellerRegisterMenuStatesGroup.register_menu.set()
