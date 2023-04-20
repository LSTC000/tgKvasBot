from data.config import ROW_WIDTH

from data.callbacks import (
    BUYER_CHANGE_CITY_DATA,
    BUYER_CHANGE_BRAND_DATA,
    BUYER_RESET_BRAND_DATA,
    CANCEL_TO_MAIN_MENU_DATA
)

from data.messages import (
    BUYER_CHANGE_CITY_IKB_MESSAGE,
    BUYER_CHANGE_BRAND_IKB_MESSAGE,
    BUYER_RESET_BRAND_IKB_MESSAGE,
    CANCEL_TO_MAIN_MENU_IKB_MESSAGE
)

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton


def buyer_settings_menu_ikb(alert_ikb_message: str, alert_data: str) -> InlineKeyboardMarkup:
    """
    :param alert_ikb_message: ON_ALERT_IKB_MESSAGE или OFF_ALERT_IKB_MESSAGE в
        data/messages/keyboards/keyboards_messages.
    :param alert_data: ON_ALERT_DATA или OFF_ALERT_DATA в data/callbacks/callbacks_data.
    :return: Клавиатура настроек покупателей.
    """

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(InlineKeyboardButton(text=BUYER_CHANGE_CITY_IKB_MESSAGE, callback_data=BUYER_CHANGE_CITY_DATA))
    ikb.row(InlineKeyboardButton(text=BUYER_CHANGE_BRAND_IKB_MESSAGE, callback_data=BUYER_CHANGE_BRAND_DATA))
    ikb.row(InlineKeyboardButton(text=BUYER_RESET_BRAND_IKB_MESSAGE, callback_data=BUYER_RESET_BRAND_DATA))
    ikb.row(InlineKeyboardButton(text=alert_ikb_message, callback_data=alert_data))
    ikb.row(InlineKeyboardButton(text=CANCEL_TO_MAIN_MENU_IKB_MESSAGE, callback_data=CANCEL_TO_MAIN_MENU_DATA))

    return ikb
