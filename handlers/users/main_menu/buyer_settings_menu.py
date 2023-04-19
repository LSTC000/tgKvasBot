from loader import dp, bot

from data.redis import LAST_IKB_REDIS_KEY

from data.callbacks import BUYER_SETTINGS_MENU_DATA, ON_ALERT_DATA, OFF_ALERT_DATA

from data.messages import BUYER_SETTINGS_MENU_MESSAGE, ON_ALERT_IKB_MESSAGE, OFF_ALERT_IKB_MESSAGE

from functions import is_alert

from keyboards import buyer_settings_menu_ikb

from states import MainMenuStatesGroup, BuyerSettingsStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda c: c.data == BUYER_SETTINGS_MENU_DATA, state=MainMenuStatesGroup.main_menu)
async def buyer_settings_menu(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Проверяем включены ли у пользователя уведомления.
    check_alert = await is_alert(user_id=user_id)

    async with state.proxy() as data:
        if LAST_IKB_REDIS_KEY in data:
            await bot.delete_message(chat_id=user_id, message_id=data[LAST_IKB_REDIS_KEY])

        # Вызываем настройки покупателя.
        msg = await bot.send_message(
            chat_id=user_id,
            text=BUYER_SETTINGS_MENU_MESSAGE,
            reply_markup=buyer_settings_menu_ikb(
                alert_ikb_message=OFF_ALERT_IKB_MESSAGE if check_alert else ON_ALERT_IKB_MESSAGE,
                alert_data=OFF_ALERT_DATA if check_alert else ON_ALERT_DATA
            )
        )

        data[LAST_IKB_REDIS_KEY] = msg.message_id

    await BuyerSettingsStatesGroup.settings_menu.set()
