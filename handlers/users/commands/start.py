from loader import dp, bot

from data.redis import LAST_IKB_REDIS_KEY

from data.messages import START_MESSAGE

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound


@dp.message_handler(commands=['start'], state='*')
async def start_command(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    async with state.proxy() as data:
        if LAST_IKB_REDIS_KEY in data:
            try:
                await bot.delete_message(chat_id=user_id, message_id=data[LAST_IKB_REDIS_KEY])
            except MessageToDeleteNotFound:
                pass

        data.clear()

    await bot.send_message(chat_id=user_id, text=START_MESSAGE.format(message.from_user.first_name))
