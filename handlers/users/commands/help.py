from loader import dp, bot

from data.messages import HELP_MESSAGE

from aiogram import types


@dp.message_handler(commands=['help'], state='*')
async def help_command(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id, text=HELP_MESSAGE)
