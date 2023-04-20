from loader import dp

from data.callbacks import BUYER_SETTINGS_MENU_DATA, ON_ALERT_DATA, OFF_ALERT_DATA

from data.messages import BUYER_SETTINGS_MENU_MESSAGE, ON_ALERT_IKB_MESSAGE, OFF_ALERT_IKB_MESSAGE

from functions import is_alert, reload_ikb

from keyboards import buyer_settings_menu_ikb

from states import MainMenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda c: c.data == BUYER_SETTINGS_MENU_DATA, state=MainMenuStatesGroup.main_menu)
async def buyer_settings_menu(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Проверяем включены ли у пользователя уведомления.
    check_alert = await is_alert(user_id=user_id)

    # Вызываем меню настроек покупателя.
    await reload_ikb(
        user_id=user_id,
        text=BUYER_SETTINGS_MENU_MESSAGE,
        new_ikb=buyer_settings_menu_ikb,
        state=state,
        ikb_params={
            'alert_ikb_message': OFF_ALERT_IKB_MESSAGE if check_alert else ON_ALERT_IKB_MESSAGE,
            'alert_data': OFF_ALERT_DATA if check_alert else ON_ALERT_DATA
        }
    )

    await MainMenuStatesGroup.settings_menu.set()
