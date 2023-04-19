from loader import dp, bot, buyer_cache

from data.messages import MENU_MESSAGE, BUYER_REGISTER_MESSAGE

from data.redis import LAST_IKB_REDIS_KEY

from keyboards import main_menu_ikb, buyer_register_menu_ikb

from functions import is_buyer

from states import MainMenuStatesGroup, BuyerRegisterMenuStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.message_handler(commands=['menu'], state='*')
async def menu_command(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    if user_id in buyer_cache:
        async with state.proxy() as data:
            if LAST_IKB_REDIS_KEY in data:
                await bot.delete_message(chat_id=user_id, message_id=data[LAST_IKB_REDIS_KEY])

            data.clear()

            msg = await bot.send_message(chat_id=user_id, text=MENU_MESSAGE, reply_markup=main_menu_ikb())
            data[LAST_IKB_REDIS_KEY] = msg.message_id

        await MainMenuStatesGroup.main_menu.set()
    elif await is_buyer(user_id):
        buyer_cache[user_id] = None

        async with state.proxy() as data:
            if LAST_IKB_REDIS_KEY in data:
                await bot.delete_message(chat_id=user_id, message_id=data[LAST_IKB_REDIS_KEY])

            data.clear()

            msg = await bot.send_message(chat_id=user_id, text=MENU_MESSAGE, reply_markup=main_menu_ikb())
            data[LAST_IKB_REDIS_KEY] = msg.message_id

        await MainMenuStatesGroup.main_menu.set()
    else:
        async with state.proxy() as data:
            if LAST_IKB_REDIS_KEY in data:
                await bot.delete_message(chat_id=user_id, message_id=data[LAST_IKB_REDIS_KEY])

            msg = await bot.send_message(
                chat_id=user_id,
                text=BUYER_REGISTER_MESSAGE,
                reply_markup=buyer_register_menu_ikb()
            )
            data[LAST_IKB_REDIS_KEY] = msg.message_id

        await BuyerRegisterMenuStatesGroup.register_menu.set()
