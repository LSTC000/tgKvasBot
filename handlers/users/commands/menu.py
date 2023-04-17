from loader import dp, bot

from data.messages import MENU_MESSAGE

from data.redis import LAST_IKB_KEY

from keyboards import main_menu_ikb

from states import MainMenuStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.message_handler(commands=['menu'], state='*')
async def menu_command(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    async with state.proxy() as data:
        if LAST_IKB_KEY in data:
            await bot.delete_message(chat_id=user_id, message_id=data[LAST_IKB_KEY])

        msg = await bot.send_message(chat_id=user_id, text=MENU_MESSAGE, reply_markup=main_menu_ikb())
        data[LAST_IKB_KEY] = msg.message_id

    await MainMenuStatesGroup.main_menu.set()
