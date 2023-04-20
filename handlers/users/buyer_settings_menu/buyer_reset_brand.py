from loader import dp, bot

from data.callbacks import BUYER_RESET_BRAND_DATA, ON_ALERT_DATA, OFF_ALERT_DATA

from data.messages import (
    BUYER_SETTINGS_MENU_MESSAGE,
    BUYER_SAVE_RESET_BRAND_MESSAGE,
    ON_ALERT_IKB_MESSAGE,
    OFF_ALERT_IKB_MESSAGE
)

from database import update_buyer_brand

from functions import is_alert, reload_ikb

from keyboards import buyer_settings_menu_ikb

from states import MainMenuStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda c: c.data == BUYER_RESET_BRAND_DATA, state=MainMenuStatesGroup.settings_menu)
async def buyer_reset_brand(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Сбрасываем бренд покупателя и отправляем ему об этом сообщение.
    await update_buyer_brand(buyer_id=user_id, brand=None)
    await bot.send_message(chat_id=user_id, text=BUYER_SAVE_RESET_BRAND_MESSAGE)

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
