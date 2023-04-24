from loader import dp, bot

from data.redis import (
    LAST_IKB_REDIS_KEY,
    LAST_RKB_REDIS_KEY,
    CITY_REGISTER_REDIS_KEY,
    BRAND_REGISTER_REDIS_KEY,
    IKB_PAGE_REDIS_KEY,
    NEAREST_SELLERS_REDIS_KEY
)

from data.messages import START_MESSAGE

from keyboards import start_command_menu_ikb

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound


@dp.message_handler(commands=['start'], state='*')
async def start_command(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    # Удаляем старую ikb и rkb клавиатуры.
    async with state.proxy() as data:
        if LAST_IKB_REDIS_KEY in data:
            try:
                await bot.delete_message(chat_id=user_id, message_id=data[LAST_IKB_REDIS_KEY])
            except MessageToDeleteNotFound:
                pass
        if LAST_RKB_REDIS_KEY in data:
            try:
                await bot.delete_message(chat_id=user_id, message_id=data[LAST_RKB_REDIS_KEY])
            except MessageToDeleteNotFound:
                pass

        if CITY_REGISTER_REDIS_KEY in data:
            data.pop(CITY_REGISTER_REDIS_KEY)

        if BRAND_REGISTER_REDIS_KEY in data:
            data.pop(BRAND_REGISTER_REDIS_KEY)

        if IKB_PAGE_REDIS_KEY in data:
            data.pop(IKB_PAGE_REDIS_KEY)

        if NEAREST_SELLERS_REDIS_KEY in data:
            data.pop(NEAREST_SELLERS_REDIS_KEY)

        data.clear()

        msg = await bot.send_message(
            chat_id=user_id,
            text=START_MESSAGE.format(message.from_user.first_name),
            reply_markup=start_command_menu_ikb()
        )

        data[LAST_IKB_REDIS_KEY] = msg.message_id
