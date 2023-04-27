from loader import dp, bot

from data.redis import LAST_IKB_REDIS_KEY

from data.messages import START_MESSAGE

from functions import keyboards_clear

from keyboards import start_command_menu_ikb

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.message_handler(commands=['start'], state='*')
async def start_command(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    # Удаляем все старые клавиатуры.
    await keyboards_clear(user_id, state)

    # Очищаем redis и вызываем start меню.
    async with state.proxy() as data:
        data.clear()

        msg = await bot.send_message(
            chat_id=user_id,
            text=START_MESSAGE.format(message.from_user.first_name),
            reply_markup=start_command_menu_ikb()
        )

        data[LAST_IKB_REDIS_KEY] = msg.message_id
