from loader import dp, bot

from data.messages import (
    MAIN_MENU_MESSAGE,
    FIND_NEAREST_SELLER_MESSAGE,
    AWAIT_FIND_NEAREST_SELLER_MESSAGE,
    NONE_NEAREST_SELLER_MESSAGE
)

from data.redis import (
    LAST_IKB_REDIS_KEY,
    LAST_RKB_REDIS_KEY,
    LAST_SEND_LOCATION_IKB_REDIS_KEY,
    LAST_SELLER_INFO_REDIS_KEY,
    IKB_PAGE_REDIS_KEY
)

from keyboards import main_menu_ikb, buyer_find_nearest_seller_menu_rkb

from functions import reload_ikb, reload_rkb, get_nearest_sellers

from inline_pickers import InlineSellerPicker

from states import MainMenuStatesGroup

from utils import create_nearest_seller_report

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound


@dp.message_handler(content_types=types.ContentTypes.LOCATION, state=MainMenuStatesGroup.main_menu)
async def find_nearest_seller(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    loading_msg = await bot.send_message(chat_id=user_id, text=AWAIT_FIND_NEAREST_SELLER_MESSAGE)

    # Достаём широту и долготу покупателя.
    latitude = message.location.latitude
    longitude = message.location.longitude

    # Достаём список доступных продавцов и запоминаем в redis страницу.
    nearest_sellers = await get_nearest_sellers(user_id, latitude, longitude, state)

    # Если существуют доступные продавцы.
    if nearest_sellers is not None:
        # Удаляем старую ikb и rkb клавиатуры.
        async with state.proxy() as data:
            if LAST_IKB_REDIS_KEY in data:
                try:
                    await bot.delete_message(chat_id=user_id, message_id=data[LAST_IKB_REDIS_KEY])
                except MessageToDeleteNotFound:
                    pass
            if LAST_RKB_REDIS_KEY in data:
                try:
                    await bot.delete_message(chat_id=user_id, message_id=data[LAST_RKB_REDIS_KEY])
                except MessageToDeleteNotFound:
                    pass

            data[IKB_PAGE_REDIS_KEY] = 0

            # Вызываем меню выбора продавца.
            msg_info = await bot.send_message(chat_id=user_id, text=create_nearest_seller_report(nearest_sellers[0][0]))
            msg_location = await bot.send_location(
                chat_id=user_id,
                latitude=nearest_sellers[0][0]['latitude'],
                longitude=nearest_sellers[0][0]['longitude'],
                reply_markup=await InlineSellerPicker().start_seller_picker(nearest_sellers=nearest_sellers, page=0)
            )

            data[LAST_SELLER_INFO_REDIS_KEY] = msg_info.message_id
            data[LAST_SEND_LOCATION_IKB_REDIS_KEY] = msg_location.message_id

            await MainMenuStatesGroup.find_nearest_seller.set()
    else:
        # Говорим покупателю, что нет доступных продавцов.
        await bot.send_message(chat_id=user_id, text=NONE_NEAREST_SELLER_MESSAGE)

        # Вызываем главное меню.
        await reload_ikb(user_id=user_id, text=MAIN_MENU_MESSAGE, new_ikb=main_menu_ikb, state=state)
        await reload_rkb(
            user_id=user_id,
            text=FIND_NEAREST_SELLER_MESSAGE,
            new_rkb=buyer_find_nearest_seller_menu_rkb,
            state=state
        )

    await bot.delete_message(chat_id=user_id, message_id=loading_msg.message_id)


@dp.callback_query_handler(state=MainMenuStatesGroup.find_nearest_seller)
async def find_next_nearest_seller(callback: types.CallbackQuery, state: FSMContext) -> None:
    # Принимаем ответ от меню выбора покупателя.
    await InlineSellerPicker().process_selection(
        callback=callback,
        callback_data=callback.data,
        state=state
    )
