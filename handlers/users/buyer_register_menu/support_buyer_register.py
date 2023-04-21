from loader import dp, bot

from data.callbacks import SUPPORT_BUYER_REGISTER_DATA

from data.messages import SUPPORT_BUYER_REGISTER_MESSAGE, BUYER_REGISTER_MENU_MESSAGE

from functions import reload_ikb

from keyboards import buyer_register_menu_ikb

from states import BuyerRegisterMenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(
    lambda c: c.data == SUPPORT_BUYER_REGISTER_DATA,
    state=BuyerRegisterMenuStatesGroup.register_menu
)
async def support_buyer_register(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Показываем пользователю справку регистрации покупателя.
    await bot.send_message(chat_id=user_id, text=SUPPORT_BUYER_REGISTER_MESSAGE)

    # Вызываем меню регистрации покупателя.
    await reload_ikb(user_id=user_id, text=BUYER_REGISTER_MENU_MESSAGE, new_ikb=buyer_register_menu_ikb, state=state)

    await BuyerRegisterMenuStatesGroup.register_menu.set()
