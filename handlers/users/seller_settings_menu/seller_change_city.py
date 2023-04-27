from loader import dp, bot

from data.redis import LAST_IKB_REDIS_KEY, IKB_PAGE_REDIS_KEY

from data.callbacks import SELLER_CHANGE_CITY_DATA

from data.messages import SELLER_SETTINGS_MENU_MESSAGE, SELLER_CHANGE_CITY_MESSAGE, SELLER_SAVE_CHANGE_CITY_MESSAGE

from functions import get_cities_from_cache, update_seller_brand_from_cache, reload_ikb

from keyboards import seller_settings_menu_ikb

from states import SellerMenuStatesGroup, SellerSettingsStatesGroup

from inline_pickers import InlineCityPicker

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound


@dp.callback_query_handler(lambda c: c.data == SELLER_CHANGE_CITY_DATA, state=SellerMenuStatesGroup.settings_menu)
async def seller_change_city(callback: types.CallbackQuery, state: FSMContext) -> None:
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
            text=SELLER_CHANGE_CITY_MESSAGE,
            reply_markup=await InlineCityPicker().start_city_picker(cities=cities, page=0)
        )

        data[LAST_IKB_REDIS_KEY] = msg.message_id

    await SellerSettingsStatesGroup.change_city.set()


@dp.callback_query_handler(state=SellerSettingsStatesGroup.change_city)
async def enter_seller_change_city(callback: types.CallbackQuery, state: FSMContext) -> None:
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
            # Обновляем город продавца в БД и отправляем ему об этом сообщение.
            await update_seller_brand_from_cache(seller_id=user_id, city=city)
            await bot.send_message(chat_id=user_id, text=SELLER_SAVE_CHANGE_CITY_MESSAGE)

        # Удаляем страницу из redis.
        async with state.proxy() as data:
            data.pop(IKB_PAGE_REDIS_KEY)

        # Вызываем меню настроек продавца.
        await reload_ikb(
            user_id=user_id,
            text=SELLER_SETTINGS_MENU_MESSAGE,
            new_ikb=seller_settings_menu_ikb,
            state=state
        )

        await SellerMenuStatesGroup.settings_menu.set()
