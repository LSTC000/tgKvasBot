from loader import dp, bot

from data.redis import LAST_IKB_REDIS_KEY, IKB_PAGE_REDIS_KEY, BRAND_REGISTER_REDIS_KEY

from data.callbacks import SELLER_CHOICE_BRAND_DATA

from data.messages import SELLER_REGISTER_MENU_MESSAGE, SELLER_CHOICE_BRAND_MESSAGE, SELLER_SAVE_CHOICE_BRAND_MESSAGE

from functions import get_brands_from_cache, reload_ikb

from keyboards import seller_register_menu_ikb

from states import SellerRegisterMenuStatesGroup

from inline_pickers import InlineBrandPicker

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound, MessageCantBeDeleted


@dp.callback_query_handler(
    lambda c: c.data == SELLER_CHOICE_BRAND_DATA,
    state=SellerRegisterMenuStatesGroup.register_menu
)
async def seller_choice_brand(callback: types.CallbackQuery, state: FSMContext) -> None:
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

        # Вызываем меню выбора бренда.
        msg = await bot.send_message(
            chat_id=user_id,
            text=SELLER_CHOICE_BRAND_MESSAGE,
            reply_markup=await InlineBrandPicker().start_brand_picker(brands=brands, page=0)
        )

        data[LAST_IKB_REDIS_KEY] = msg.message_id

    await SellerRegisterMenuStatesGroup.choice_brand.set()


@dp.callback_query_handler(state=SellerRegisterMenuStatesGroup.choice_brand)
async def enter_seller_choice_brand(callback: types.CallbackQuery, state: FSMContext) -> None:
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

        if brand is not None:
            # Добавляем в redis выбранный бренд и отправляем об этом сообщение.
            async with state.proxy() as data:
                data[BRAND_REGISTER_REDIS_KEY] = brand
                await bot.send_message(chat_id=user_id, text=SELLER_SAVE_CHOICE_BRAND_MESSAGE)

        # Удаляем страницу из redis.
        async with state.proxy() as data:
            data.pop(IKB_PAGE_REDIS_KEY)

        # Вызываем меню для регистрации.
        await reload_ikb(
            user_id=user_id,
            text=SELLER_REGISTER_MENU_MESSAGE,
            new_ikb=seller_register_menu_ikb,
            state=state
        )

        await SellerRegisterMenuStatesGroup.register_menu.set()
