from loader import dp, bot

from data.redis import LAST_IKB_REDIS_KEY, IKB_PAGE_REDIS_KEY

from data.callbacks import BUYER_CHANGE_BRAND_DATA

from data.messages import BUYER_SETTINGS_MENU_MESSAGE, BUYER_CHANGE_BRAND_MESSAGE, BUYER_SAVE_CHANGE_BRAND_MESSAGE

from functions import (
    get_brands_from_cache,
    update_buyer_brand_from_cache,
    reload_ikb,
    get_buyer_settings_menu_ikb_params
)

from keyboards import buyer_settings_menu_ikb

from states import MainMenuStatesGroup, BuyerSettingsStatesGroup

from inline_pickers import InlineBrandPicker

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound, MessageCantBeDeleted


@dp.callback_query_handler(lambda c: c.data == BUYER_CHANGE_BRAND_DATA, state=MainMenuStatesGroup.settings_menu)
async def buyer_change_brand(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    async with state.proxy() as data:
        if LAST_IKB_REDIS_KEY in data:
            try:
                await bot.delete_message(chat_id=user_id, message_id=data[LAST_IKB_REDIS_KEY])
            except (MessageToDeleteNotFound, MessageCantBeDeleted):
                pass

        # Достаём список доступных брендов и запоминаем в redis страницу.
        brands = await get_brands_from_cache()
        data[IKB_PAGE_REDIS_KEY] = 0

        # Вызываем меню выбора города.
        msg = await bot.send_message(
            chat_id=user_id,
            text=BUYER_CHANGE_BRAND_MESSAGE,
            reply_markup=await InlineBrandPicker().start_brand_picker(brands=brands, page=0)
        )

        data[LAST_IKB_REDIS_KEY] = msg.message_id

    await BuyerSettingsStatesGroup.change_brand.set()


@dp.callback_query_handler(state=BuyerSettingsStatesGroup.change_brand)
async def enter_buyer_change_brand(callback: types.CallbackQuery, state: FSMContext) -> None:
    # Достаём список доступных брендов.
    brands = await get_brands_from_cache()

    # Принимаем ответ от меню выбора бренда.
    selected, brand = await InlineBrandPicker().process_selection(
        brands=brands,
        callback=callback,
        callback_data=callback.data,
        state=state
    )

    # Проверяем получили ли мы бренд от пользователя.
    if selected:
        user_id = callback.from_user.id

        if brand is not None:
            # Обновляем бренд покупателя в БД и отправляем ему об этом сообщение.
            await update_buyer_brand_from_cache(buyer_id=user_id, brand=brand)
            await bot.send_message(chat_id=user_id, text=BUYER_SAVE_CHANGE_BRAND_MESSAGE)

        # Удаляем страницу из redis.
        async with state.proxy() as data:
            data.pop(IKB_PAGE_REDIS_KEY)

        # Вызываем меню настроек покупателя.
        await reload_ikb(
            user_id=user_id,
            text=BUYER_SETTINGS_MENU_MESSAGE,
            new_ikb=buyer_settings_menu_ikb,
            state=state,
            ikb_params=await get_buyer_settings_menu_ikb_params(user_id)
        )

        await MainMenuStatesGroup.settings_menu.set()
