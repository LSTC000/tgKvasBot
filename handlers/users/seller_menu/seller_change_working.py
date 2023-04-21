from loader import dp, bot

from data.redis import LAST_IKB_REDIS_KEY

from data.callbacks import START_WORKING_DATA, STOP_WORKING_DATA

from database import update_seller_working

from keyboards import seller_menu_ikb

from functions import get_seller_menu_ikb_params

from states import MainMenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(
    lambda c: c.data in [START_WORKING_DATA, STOP_WORKING_DATA],
    state=MainMenuStatesGroup.seller_menu
)
async def seller_change_working(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    if callback.data == START_WORKING_DATA:
        # Запоминаем, что продавец начал работу.
        await update_seller_working(seller_id=user_id, working=1)
    else:
        # Запоминаем, что продавец прекратил работу.
        await update_seller_working(seller_id=user_id, working=0)

    async with state.proxy() as data:
        # Обновляем меню продавца.
        await bot.edit_message_reply_markup(
            chat_id=user_id,
            message_id=data[LAST_IKB_REDIS_KEY],
            reply_markup=seller_menu_ikb(**await get_seller_menu_ikb_params(user_id))
        )

    await MainMenuStatesGroup.seller_menu.set()
