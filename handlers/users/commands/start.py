from loader import dp, bot

from data.messages import START_MESSAGE

from aiogram import types


@dp.message_handler(commands=['start'], state='*')
async def start_command(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id, text=START_MESSAGE.format(message.from_user.first_name))
