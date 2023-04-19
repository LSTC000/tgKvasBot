from loader import dp, bot

from data.redis import LAST_IKB_REDIS_KEY

from data.callbacks import SUPPORT_BUYER_REGISTER_DATA

from data.messages import SUPPORT_BUYER_REGISTER_MESSAGE, BUYER_REGISTER_MESSAGE

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

    async with state.proxy() as data:
        if LAST_IKB_REDIS_KEY in data:
            await bot.delete_message(chat_id=user_id, message_id=data[LAST_IKB_REDIS_KEY])

        # Показываем пользователю справку регистрации покупателя.
        await bot.send_message(chat_id=user_id, text=SUPPORT_BUYER_REGISTER_MESSAGE)

        # Вызываем меню регистрации покупателя.
        msg = await bot.send_message(
            chat_id=user_id,
            text=BUYER_REGISTER_MESSAGE,
            reply_markup=buyer_register_menu_ikb()
        )

        data[LAST_IKB_REDIS_KEY] = msg.message_id

    await BuyerRegisterMenuStatesGroup.register_menu.set()
