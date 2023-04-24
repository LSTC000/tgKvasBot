from data.callbacks import CANCEL_TO_MAIN_MENU_DATA

from data.config import SELLER_PICKER_ROW_WIDTH

from data.messages import CANCEL_TO_MAIN_MENU_IKB_MESSAGE

from data.redis import (
    IKB_PAGE_REDIS_KEY,
    LAST_SEND_LOCATION_IKB_REDIS_KEY,
    LAST_SELLER_INFO_REDIS_KEY,
    NEAREST_SELLERS_REDIS_KEY
)

from loader import bot

from utils import create_nearest_seller_report

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import MessageToDeleteNotFound


class InlineSellerPicker:
    async def start_seller_picker(
            self,
            nearest_sellers: list,
            page: int
    ) -> InlineKeyboardMarkup:
        """
        :param nearest_sellers: Список продавцов.
        :param page: Страница inline клавиатуры. В начале: 0.
        :return: Клавиатура с меню поиска продавца.
        """

        inline_kb = InlineKeyboardMarkup(row_width=SELLER_PICKER_ROW_WIDTH)
        ignore_callback = "IGNORE"

        count_nearest_sellers = len(nearest_sellers)

        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(
            text="<<" if page != 0 else " ",
            callback_data="PREV-SELLER" if page != 0 else ignore_callback
        ))
        inline_kb.insert(InlineKeyboardButton(" ", callback_data=ignore_callback))
        inline_kb.insert(InlineKeyboardButton(
            text=">>" if page != count_nearest_sellers - 1 else " ",
            callback_data="NEXT-SELLER" if page != count_nearest_sellers - 1 else ignore_callback
        ))

        inline_kb.row(InlineKeyboardButton(CANCEL_TO_MAIN_MENU_IKB_MESSAGE, callback_data=CANCEL_TO_MAIN_MENU_DATA))

        return inline_kb

    async def process_selection(
            self,
            callback: types.CallbackQuery,
            callback_data: str,
            state: FSMContext
    ) -> None:
        """
        :param callback: Callback содержащий клавиатуру с меню ближайшего продавца.
        :param callback_data: Действие, выбранное пользователем.
        :param state: FSMContext.
        """

        async with state.proxy() as data:
            page = data[IKB_PAGE_REDIS_KEY]
            nearest_sellers = data[NEAREST_SELLERS_REDIS_KEY]

            user_id = callback.from_user.id

            if callback_data == "IGNORE":
                await callback.answer(cache_time=60)

            if callback_data == "PREV-SELLER":
                page -= 1
                data[IKB_PAGE_REDIS_KEY] = page

                if LAST_SELLER_INFO_REDIS_KEY in data:
                    try:
                        await bot.delete_message(chat_id=user_id, message_id=data[LAST_SELLER_INFO_REDIS_KEY])
                    except MessageToDeleteNotFound:
                        pass
                if LAST_SEND_LOCATION_IKB_REDIS_KEY in data:
                    try:
                        await bot.delete_message(chat_id=user_id, message_id=data[LAST_SEND_LOCATION_IKB_REDIS_KEY])
                    except MessageToDeleteNotFound:
                        pass

                msg_info = await bot.send_message(
                    chat_id=user_id,
                    text=create_nearest_seller_report(nearest_sellers[page][0])
                )
                msg_location = await bot.send_location(
                    chat_id=user_id,
                    latitude=nearest_sellers[page][0]['latitude'],
                    longitude=nearest_sellers[page][0]['longitude'],
                    reply_markup=await InlineSellerPicker().start_seller_picker(
                        nearest_sellers=nearest_sellers,
                        page=page
                    )
                )

                data[LAST_SELLER_INFO_REDIS_KEY] = msg_info.message_id
                data[LAST_SEND_LOCATION_IKB_REDIS_KEY] = msg_location.message_id

            if callback_data == "NEXT-SELLER":
                page += 1
                data[IKB_PAGE_REDIS_KEY] = page

                if LAST_SELLER_INFO_REDIS_KEY in data:
                    try:
                        await bot.delete_message(chat_id=user_id, message_id=data[LAST_SELLER_INFO_REDIS_KEY])
                    except MessageToDeleteNotFound:
                        pass
                if LAST_SEND_LOCATION_IKB_REDIS_KEY in data:
                    try:
                        await bot.delete_message(chat_id=user_id, message_id=data[LAST_SEND_LOCATION_IKB_REDIS_KEY])
                    except MessageToDeleteNotFound:
                        pass

                msg_info = await bot.send_message(
                    chat_id=user_id,
                    text=create_nearest_seller_report(nearest_sellers[page][0])
                )
                msg_location = await bot.send_location(
                    chat_id=user_id,
                    latitude=nearest_sellers[page][0]['latitude'],
                    longitude=nearest_sellers[page][0]['longitude'],
                    reply_markup=await InlineSellerPicker().start_seller_picker(
                        nearest_sellers=nearest_sellers,
                        page=page
                    )
                )

                data[LAST_SELLER_INFO_REDIS_KEY] = msg_info.message_id
                data[LAST_SEND_LOCATION_IKB_REDIS_KEY] = msg_location.message_id
