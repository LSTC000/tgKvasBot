from loader import dp

from data.callbacks import CANCEL_TO_MAIN_MENU_DATA

from data.messages import MENU_MESSAGE

from functions import reload_ikb

from keyboards import main_menu_ikb

from states import MainMenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(
    lambda c: c.data == CANCEL_TO_MAIN_MENU_DATA,
    state=MainMenuStatesGroup.settings_menu
)
async def cancel_to_main_menu(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Вызываем главное меню.
    await reload_ikb(user_id=user_id, text=MENU_MESSAGE, new_ikb=main_menu_ikb, state=state)

    await MainMenuStatesGroup.main_menu.set()
