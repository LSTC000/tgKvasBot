from typing import List

from data.callbacks import CANCEL_TO_LAST_MENU_DATA

from data.config import BRAND_PICKER_ROW_WIDTH, MAX_BRANDS_ON_PAGE

from data.messages import CANCEL_TO_LAST_MENU_IKB_MESSAGE

from data.redis import IKB_PAGE_REDIS_KEY

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class InlineBrandPicker:
    async def start_brand_picker(self, brands: List[str], page: int) -> InlineKeyboardMarkup:
        """
        :param brands: Список брендов.
        :param page: Страница inline клавиатуры. В начале: 0.
        :return: Клавиатура с меню выбора бренда.
        """

        inline_kb = InlineKeyboardMarkup(row_width=BRAND_PICKER_ROW_WIDTH)
        ignore_callback = "IGNORE"

        count_brands = len(brands)
        start = page * MAX_BRANDS_ON_PAGE
        stop = start + MAX_BRANDS_ON_PAGE

        for i in range(start, stop if stop <= count_brands else count_brands):
            inline_kb.row(InlineKeyboardButton(
                    text=brands[i],
                    callback_data=brands[i]
                ))

        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(
            text="<<" if page != 0 else " ",
            callback_data="PREV-BRANDS" if page != 0 else ignore_callback
        ))
        inline_kb.insert(InlineKeyboardButton(" ", callback_data=ignore_callback))
        inline_kb.insert(InlineKeyboardButton(
            text=">>" if count_brands > stop else " ",
            callback_data="NEXT-BRANDS" if count_brands > stop else ignore_callback
        ))

        inline_kb.row(InlineKeyboardButton(CANCEL_TO_LAST_MENU_IKB_MESSAGE, callback_data=CANCEL_TO_LAST_MENU_DATA))

        return inline_kb

    async def process_selection(
            self,
            brands: list,
            callback: types.CallbackQuery,
            callback_data: str,
            state: FSMContext
    ) -> tuple:
        """
        :param brands: Список брендов.
        :param callback: Callback содержащий клавиатуру с меню выбора города.
        :param callback_data: Действие, выбранное пользователем.
        :param state: FSMContext.
        :return: Кортеж, в котором первый элемент имеет значение True, если пользователь выбрал бренд
             или возврат в предыдущее меню и False иначе. Второй элемент содержит строку с выбранным брендом или None,
             если пользователь выбрал возврат в предыдущее меню.
        """

        async with state.proxy() as data:
            page = data[IKB_PAGE_REDIS_KEY]

            return_data = False, None

            if callback_data == "IGNORE":
                await callback.answer(cache_time=60)
            elif callback_data == "PREV-BRANDS":
                page -= 1
                data[IKB_PAGE_REDIS_KEY] = page
                await callback.message.edit_reply_markup(await self.start_brand_picker(brands=brands, page=page))
            elif callback_data == "NEXT-BRANDS":
                page += 1
                data[IKB_PAGE_REDIS_KEY] = page
                await callback.message.edit_reply_markup(await self.start_brand_picker(brands=brands, page=page))
            elif callback_data == CANCEL_TO_LAST_MENU_DATA:
                return True, None
            else:
                return_data = True, callback_data

        return return_data
