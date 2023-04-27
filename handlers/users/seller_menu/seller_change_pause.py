from loader import dp, bot

from data.redis import LAST_IKB_REDIS_KEY

from data.callbacks import START_PAUSE_DATA, STOP_PAUSE_DATA

from keyboards import seller_menu_ikb

from functions import get_seller_menu_ikb_params, update_seller_pause_from_cache

from states import MainMenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(
    lambda c: c.data in [START_PAUSE_DATA, STOP_PAUSE_DATA],
    state=MainMenuStatesGroup.seller_menu
)
async def seller_change_pause(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    if callback.data == START_PAUSE_DATA:
        # Запоминаем, что продавец ушёл на перерыв.
        await update_seller_pause_from_cache(seller_id=user_id, pause=1)
    else:
        # Запоминаем, что продавец вышел с перерыва.
        await update_seller_pause_from_cache(seller_id=user_id, pause=0)

    async with state.proxy() as data:
        # Обновляем меню продавца.
        await bot.edit_message_reply_markup(
            chat_id=user_id,
            message_id=data[LAST_IKB_REDIS_KEY],
            reply_markup=seller_menu_ikb(**await get_seller_menu_ikb_params(user_id))
        )

    await MainMenuStatesGroup.seller_menu.set()
