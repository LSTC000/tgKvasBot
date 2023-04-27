from loader import dp, bot

from data.redis import LAST_IKB_REDIS_KEY

from data.callbacks import AVAILABILITY_DATA, UNAVAILABILITY_DATA

from keyboards import seller_menu_ikb

from functions import get_seller_menu_ikb_params, update_seller_availability_from_cache

from states import MainMenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(
    lambda c: c.data in [AVAILABILITY_DATA, UNAVAILABILITY_DATA],
    state=MainMenuStatesGroup.seller_menu
)
async def seller_change_availability(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    if callback.data == AVAILABILITY_DATA:
        # Запоминаем, что у продовца есть квас.
        await update_seller_availability_from_cache(seller_id=user_id, availability=1)
    else:
        # Запоминаем, что у продовца закончился квас.
        await update_seller_availability_from_cache(seller_id=user_id, availability=0)

    async with state.proxy() as data:
        # Обновляем меню продавца.
        await bot.edit_message_reply_markup(
            chat_id=user_id,
            message_id=data[LAST_IKB_REDIS_KEY],
            reply_markup=seller_menu_ikb(**await get_seller_menu_ikb_params(user_id))
        )

    await MainMenuStatesGroup.seller_menu.set()
