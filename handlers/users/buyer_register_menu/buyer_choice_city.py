from loader import dp, bot

from data.redis import LAST_IKB_REDIS_KEY, PAGE_REDIS_KEY

from data.callbacks import BUYER_CHOICE_CITY_DATA

from data.messages import MENU_MESSAGE, BUYER_CHOICE_CITY_MESSAGE, BUYER_SAVE_CHOICE_CITY_MESSAGE

from database import add_buyer, add_alert

from functions import get_cities_from_cache, reload_ikb

from keyboards import main_menu_ikb

from states import MainMenuStatesGroup, BuyerRegisterMenuStatesGroup

from inline_pickers import InlineCityPicker

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(
    lambda c: c.data == BUYER_CHOICE_CITY_DATA,
    state=BuyerRegisterMenuStatesGroup.register_menu
)
async def buyer_choice_city(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    async with state.proxy() as data:
        if LAST_IKB_REDIS_KEY in data:
            await bot.delete_message(chat_id=user_id, message_id=data[LAST_IKB_REDIS_KEY])

        # Достаём список доступных городов и переходим на начальную страницу.
        cities = await get_cities_from_cache()
        data[PAGE_REDIS_KEY] = 0

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

        # Добавляем пользователя в БД и отправляем ему об этом сообщение.
        await add_buyer(buyer_id=user_id, city=city, brand=None)
        await bot.send_message(chat_id=user_id, text=BUYER_SAVE_CHOICE_CITY_MESSAGE)

        #Добавляем пользователя в список тех, кто будет получать уведомления.
        await add_alert(user_id=user_id)

        # Вызываем главное меню.
        await reload_ikb(user_id=user_id, text=MENU_MESSAGE, new_ikb=main_menu_ikb, state=state)

        await MainMenuStatesGroup.main_menu.set()
