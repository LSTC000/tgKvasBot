from typing import List

from data.callbacks import CANCEL_TO_LAST_MENU_DATA

from data.config import CITY_PICKER_ROW_WIDTH, MAX_CITIES_ON_PAGE

from data.messages import CANCEL_TO_LAST_MENU_IKB_MESSAGE

from data.redis import IKB_PAGE_REDIS_KEY

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class InlineCityPicker:
    async def start_city_picker(self, cities: List[str], page: int) -> InlineKeyboardMarkup:
        """
        :param cities: Список городов.
        :param page: Страница inline клавиатуры. В начале: 0.
        :return: Клавиатура с меню выбора города.
        """

        inline_kb = InlineKeyboardMarkup(row_width=CITY_PICKER_ROW_WIDTH)
        ignore_callback = "IGNORE"

        count_cities = len(cities)
        start = page * MAX_CITIES_ON_PAGE
        stop = start + MAX_CITIES_ON_PAGE

        for i in range(start, stop if stop <= count_cities else count_cities):
            inline_kb.row(InlineKeyboardButton(
                    text=cities[i],
                    callback_data=cities[i]
                ))

        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(
            text="<<" if page != 0 else " ",
            callback_data="PREV-CITIES" if page != 0 else ignore_callback
        ))
        inline_kb.insert(InlineKeyboardButton(" ", callback_data=ignore_callback))
        inline_kb.insert(InlineKeyboardButton(
            text=">>" if count_cities > stop else " ",
            callback_data="NEXT-CITIES" if count_cities > stop else ignore_callback
        ))

        inline_kb.row(InlineKeyboardButton(CANCEL_TO_LAST_MENU_IKB_MESSAGE, callback_data=CANCEL_TO_LAST_MENU_DATA))

        return inline_kb

    async def process_selection(
            self,
            cities: list,
            callback: types.CallbackQuery,
            callback_data: str,
            state: FSMContext
    ) -> tuple:
        """
        :param cities: Список городов.
        :param callback: Callback содержащий клавиатуру с меню выбора города.
        :param callback_data: Действие, выбранное пользователем.
        :param state: FSMContext.
        :return: Кортеж, в котором первый элемент имеет значение True, если пользователь выбрал город
            или возврат в предыдущее меню и False иначе. Второй элемент содержит строку с выбранным городом или None,
             если пользователь выбрал возврат в предыдущее меню.
        """

        async with state.proxy() as data:
            page = data[IKB_PAGE_REDIS_KEY]

            return_data = False, None

            if callback_data == "IGNORE":
                await callback.answer(cache_time=60)
            elif callback_data == "PREV-CITIES":
                page -= 1
                data[IKB_PAGE_REDIS_KEY] = page
                await callback.message.edit_reply_markup(await self.start_city_picker(cities=cities, page=page))
            elif callback_data == "NEXT-CITIES":
                page += 1
                data[IKB_PAGE_REDIS_KEY] = page
                await callback.message.edit_reply_markup(await self.start_city_picker(cities=cities, page=page))
            elif callback_data == CANCEL_TO_LAST_MENU_DATA:
                return True, None
            else:
                return_data = True, callback_data

        return return_data
