from loader import dp, bot

from data.redis import LAST_IKB_REDIS_KEY, IKB_PAGE_REDIS_KEY

from data.callbacks import BUYER_CHANGE_CITY_DATA, ON_ALERT_DATA, OFF_ALERT_DATA

from data.messages import (
    BUYER_SETTINGS_MENU_MESSAGE,
    BUYER_CHANGE_CITY_MESSAGE,
    BUYER_SAVE_CHANGE_CITY_MESSAGE,
    ON_ALERT_IKB_MESSAGE,
    OFF_ALERT_IKB_MESSAGE
)

from database import update_buyer_city

from functions import get_cities_from_cache, is_alert, reload_ikb

from keyboards import buyer_settings_menu_ikb

from states import MainMenuStatesGroup, BuyerSettingsStatesGroup

from inline_pickers import InlineCityPicker

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda c: c.data == BUYER_CHANGE_CITY_DATA, state=MainMenuStatesGroup.settings_menu)
async def buyer_change_city(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    async with state.proxy() as data:
        if LAST_IKB_REDIS_KEY in data:
            await bot.delete_message(chat_id=user_id, message_id=data[LAST_IKB_REDIS_KEY])

        # Достаём список доступных городов и запоминаем в redis страницу.
        cities = await get_cities_from_cache()
        data[IKB_PAGE_REDIS_KEY] = 0

        # Вызываем меню выбора города.
        msg = await bot.send_message(
            chat_id=user_id,
            text=BUYER_CHANGE_CITY_MESSAGE,
            reply_markup=await InlineCityPicker().start_citypicker(cities=cities, page=0)
        )

        data[LAST_IKB_REDIS_KEY] = msg.message_id

    await BuyerSettingsStatesGroup.change_city.set()


@dp.callback_query_handler(state=BuyerSettingsStatesGroup.change_city)
async def enter_buyer_change_city(callback: types.CallbackQuery, state: FSMContext) -> None:
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

        # Удаляем страницу из redis.
        async with state.proxy() as data:
            data.pop(IKB_PAGE_REDIS_KEY)

        # Обновляем город пользователя в БД и отправляем ему об этом сообщение.
        await update_buyer_city(buyer_id=user_id, city=city)
        await bot.send_message(chat_id=user_id, text=BUYER_SAVE_CHANGE_CITY_MESSAGE)

        # Проверяем включены ли у пользователя уведомления.
        check_alert = await is_alert(user_id=user_id)

        # Вызываем меню настроек покупателя.
        await reload_ikb(
            user_id=user_id,
            text=BUYER_SETTINGS_MENU_MESSAGE,
            new_ikb=buyer_settings_menu_ikb,
            state=state,
            ikb_params={
                'alert_ikb_message': OFF_ALERT_IKB_MESSAGE if check_alert else ON_ALERT_IKB_MESSAGE,
                'alert_data': OFF_ALERT_DATA if check_alert else ON_ALERT_DATA
            }
        )

        await MainMenuStatesGroup.settings_menu.set()