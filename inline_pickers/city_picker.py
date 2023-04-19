from typing import List

from data.config import CITY_PICKER_ROW_WIDTH, MAX_CITIES_ON_PAGE

from data.redis import PAGE_REDIS_KEY

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class InlineCityPicker:
    async def start_citypicker(self, cities: List[str], page: int) -> InlineKeyboardMarkup:
        """
        :param cities: Список городов.
        :param page: Страница inline клавиатуры. В начале: 0.
        :return: Клавиатура с меню выбора города.
        """

        inline_kb = InlineKeyboardMarkup(row_width=CITY_PICKER_ROW_WIDTH)
        ignore_callback = f"IGNORE"

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
            callback_data=f"PREV-CITIES" if page != 0 else ignore_callback
        ))
        inline_kb.insert(InlineKeyboardButton(" ", callback_data=ignore_callback))
        inline_kb.insert(InlineKeyboardButton(
            text=">>" if count_cities > stop else " ",
            callback_data=f"NEXT-CITIES" if count_cities > stop else ignore_callback
        ))

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
            и False иначе. Второй элемент содержит строку с выбранным городом.
        """

        async with state.proxy() as data:
            page = data[PAGE_REDIS_KEY]

            return_data = (False, None)

            if callback_data == "IGNORE":
                await callback.answer(cache_time=60)
            elif callback_data == "PREV-CITIES":
                page -= 1
                data[PAGE_REDIS_KEY] = page
                await callback.message.edit_reply_markup(await self.start_citypicker(cities=cities, page=page))
            elif callback_data == "NEXT-CITIES":
                page += 1
                data[PAGE_REDIS_KEY] = page
                await callback.message.edit_reply_markup(await self.start_citypicker(cities=cities, page=page))
            else:
                return_data = True, callback_data

        return return_data
