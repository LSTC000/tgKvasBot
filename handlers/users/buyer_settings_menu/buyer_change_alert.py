from loader import dp, bot

from data.redis import LAST_IKB_REDIS_KEY

from data.callbacks import ON_ALERT_DATA, OFF_ALERT_DATA

from data.messages import ON_ALERT_IKB_MESSAGE, OFF_ALERT_IKB_MESSAGE

from database import add_alert, delete_alert

from keyboards import buyer_settings_menu_ikb

from states import BuyerSettingsStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(
    lambda c: c.data in [ON_ALERT_DATA, OFF_ALERT_DATA],
    state=BuyerSettingsStatesGroup.settings_menu
)
async def buyer_change_alert(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    if callback.data == ON_ALERT_DATA:
        # Добавляем пользователя в список тех, кто получает уведомления.
        await add_alert(user_id=user_id)
        alert_ikb_message = OFF_ALERT_IKB_MESSAGE
        alert_data = OFF_ALERT_DATA
    else:
        # Удаляем пользователя из списка тех, кто получает уведомления.
        await delete_alert(user_id=user_id)
        alert_ikb_message = ON_ALERT_IKB_MESSAGE
        alert_data = ON_ALERT_DATA

    async with state.proxy() as data:
        # Обновляем меню настройки покупателя.
        await bot.edit_message_reply_markup(
            chat_id=user_id,
            message_id=data[LAST_IKB_REDIS_KEY],
            reply_markup=buyer_settings_menu_ikb(alert_ikb_message=alert_ikb_message, alert_data=alert_data)
        )

    await BuyerSettingsStatesGroup.settings_menu.set()
