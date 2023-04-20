from loader import dp, bot

from data.redis import LAST_IKB_REDIS_KEY, PAGE_REDIS_KEY

from data.callbacks import BUYER_CHOICE_BRAND_DATA

from data.messages import BUYER_MENU_IKB_MESSAGE, BUYER_CHOICE_BRAND_MESSAGE, BUYER_SAVE_CHOICE_BRAND_MESSAGE

from database import update_buyer_brand

from functions import get_brands_from_cache, reload_ikb

from keyboards import buyer_menu_ikb

from states import MainMenuStatesGroup, BuyerMenuStatesGroup

from inline_pickers import InlineBrandPicker

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda c: c.data == BUYER_CHOICE_BRAND_DATA, state=MainMenuStatesGroup.buyer_menu)
async def buyer_choice_brand(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    async with state.proxy() as data:
        if LAST_IKB_REDIS_KEY in data:
            await bot.delete_message(chat_id=user_id, message_id=data[LAST_IKB_REDIS_KEY])

        # Достаём список доступных брендов и переходим на начальную страницу.
        brands = await get_brands_from_cache()
        data[PAGE_REDIS_KEY] = 0

        # Вызываем меню выбора бренда.
        msg = await bot.send_message(
            chat_id=user_id,
            text=BUYER_CHOICE_BRAND_MESSAGE,
            reply_markup=await InlineBrandPicker().start_brandpicker(brands=brands, page=0)
        )

        data[LAST_IKB_REDIS_KEY] = msg.message_id

    await BuyerMenuStatesGroup.choice_brand.set()


@dp.callback_query_handler(state=BuyerMenuStatesGroup.choice_brand)
async def enter_buyer_choice_brand(callback: types.CallbackQuery, state: FSMContext) -> None:
    # Достаём список доступных брендов.
    brands = await get_brands_from_cache()

    # Принимаем ответ от меню выбора города.
    selected, brand = await InlineBrandPicker().process_selection(
        brands=brands,
        callback=callback,
        callback_data=callback.data,
        state=state
    )

    # Проверяем получили ли мы бренд от пользователя.
    if selected:
        user_id = callback.from_user.id

        # Обновляем бренд пользователя в БД и отправляем ему об этом сообщение.
        await update_buyer_brand(buyer_id=user_id, brand=brand)
        await bot.send_message(chat_id=user_id, text=BUYER_SAVE_CHOICE_BRAND_MESSAGE)

        # Вызываем меню для покупателя.
        await reload_ikb(user_id=user_id, text=BUYER_MENU_IKB_MESSAGE, new_ikb=buyer_menu_ikb, state=state)

        await MainMenuStatesGroup.buyer_menu.set()
