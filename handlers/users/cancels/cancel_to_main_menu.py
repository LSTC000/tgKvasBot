from loader import dp, bot

from data.redis import LAST_IKB_REDIS_KEY

from data.callbacks import CANCEL_TO_MAIN_MENU_DATA

from data.messages import MENU_MESSAGE

from keyboards import main_menu_ikb

from states import MainMenuStatesGroup, BuyerSettingsStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(
    lambda c: c.data == CANCEL_TO_MAIN_MENU_DATA,
    state=BuyerSettingsStatesGroup.settings_menu
)
async def cancel_to_main_menu(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    async with state.proxy() as data:
        if LAST_IKB_REDIS_KEY in data:
            await bot.delete_message(chat_id=user_id, message_id=data[LAST_IKB_REDIS_KEY])

        # Вызываем главное меню.
        msg = await bot.send_message(
            chat_id=user_id,
            text=MENU_MESSAGE,
            reply_markup=main_menu_ikb()
        )

        data[LAST_IKB_REDIS_KEY] = msg.message_id

    await MainMenuStatesGroup.main_menu.set()
