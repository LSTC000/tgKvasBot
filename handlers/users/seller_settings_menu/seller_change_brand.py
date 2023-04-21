from loader import dp, bot

from data.redis import LAST_IKB_REDIS_KEY, IKB_PAGE_REDIS_KEY

from data.callbacks import SELLER_CHANGE_BRAND_DATA

from data.messages import SELLER_SETTINGS_MENU_MESSAGE, SELLER_CHANGE_BRAND_MESSAGE, SELLER_SAVE_CHANGE_BRAND_MESSAGE

from database import update_seller_brand

from functions import get_brands_from_cache, reload_ikb

from keyboards import seller_settings_menu_ikb

from states import SellerMenuStatesGroup, SellerSettingsStatesGroup

from inline_pickers import InlineBrandPicker

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound


@dp.callback_query_handler(lambda c: c.data == SELLER_CHANGE_BRAND_DATA, state=SellerMenuStatesGroup.settings_menu)
async def seller_change_brand(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    async with state.proxy() as data:
        if LAST_IKB_REDIS_KEY in data:
            try:
                await bot.delete_message(chat_id=user_id, message_id=data[LAST_IKB_REDIS_KEY])
            except MessageToDeleteNotFound:
                pass

        # Достаём список доступных брендов и запоминаем в redis страницу.
        brands = await get_brands_from_cache()
        data[IKB_PAGE_REDIS_KEY] = 0

        # Вызываем меню выбора города.
        msg = await bot.send_message(
            chat_id=user_id,
            text=SELLER_CHANGE_BRAND_MESSAGE,
            reply_markup=await InlineBrandPicker().start_brandpicker(brands=brands, page=0)
        )

        data[LAST_IKB_REDIS_KEY] = msg.message_id

    await SellerSettingsStatesGroup.change_brand.set()


@dp.callback_query_handler(state=SellerSettingsStatesGroup.change_brand)
async def enter_seller_change_brand(callback: types.CallbackQuery, state: FSMContext) -> None:
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
            # Обновляем бренд продавца в БД и отправляем ему об этом сообщение.
            await update_seller_brand(seller_id=user_id, brand=brand)
            await bot.send_message(chat_id=user_id, text=SELLER_SAVE_CHANGE_BRAND_MESSAGE)

        # Удаляем страницу из redis.
        async with state.proxy() as data:
            data.pop(IKB_PAGE_REDIS_KEY)

        # Вызываем меню настроек покупателя.
        await reload_ikb(
            user_id=user_id,
            text=SELLER_SETTINGS_MENU_MESSAGE,
            new_ikb=seller_settings_menu_ikb,
            state=state
        )

        await SellerMenuStatesGroup.settings_menu.set()
