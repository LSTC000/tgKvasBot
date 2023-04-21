from loader import dp, bot

from data.callbacks import SUPPORT_SELLER_REGISTER_DATA

from data.messages import SUPPORT_SELLER_REGISTER_MESSAGE, SELLER_REGISTER_MENU_MESSAGE

from functions import reload_ikb

from keyboards import seller_register_menu_ikb

from states import SellerRegisterMenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(
    lambda c: c.data == SUPPORT_SELLER_REGISTER_DATA,
    state=SellerRegisterMenuStatesGroup.register_menu
)
async def support_seller_register(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Показываем пользователю справку регистрации продавца.
    await bot.send_message(chat_id=user_id, text=SUPPORT_SELLER_REGISTER_MESSAGE)

    # Вызываем меню регистрации продавца.
    await reload_ikb(user_id=user_id, text=SELLER_REGISTER_MENU_MESSAGE, new_ikb=seller_register_menu_ikb, state=state)

    await SellerRegisterMenuStatesGroup.register_menu.set()
