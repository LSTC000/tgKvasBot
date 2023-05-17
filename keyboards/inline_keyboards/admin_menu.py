from data.config import ROW_WIDTH

from data.callbacks import (
    COUNT_SECRET_KEYS_DATA,
    CREATE_SECRET_KEY_DATA,
    SHOW_SECRET_KEYS_DATA,
    DELETE_SECRET_KEYS_DATA,
    ALERT_FOR_USERS_DATA
)

from data.messages import (
    COUNT_SECRET_KEYS_IKB_MESSAGE,
    CREATE_SECRET_KEYS_IKB_MESSAGE,
    SHOW_SECRET_KEYS_IKB_MESSAGE,
    DELETE_SECRET_KEYS_IKB_MESSAGE,
    ALERT_FOR_USERS_IKB_MESSAGE
)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_menu_ikb() -> InlineKeyboardMarkup:
    """
    :return: Клавиатура меню администратора.
    """

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(InlineKeyboardButton(text=COUNT_SECRET_KEYS_IKB_MESSAGE, callback_data=COUNT_SECRET_KEYS_DATA))
    ikb.row(InlineKeyboardButton(text=CREATE_SECRET_KEYS_IKB_MESSAGE, callback_data=CREATE_SECRET_KEY_DATA))
    ikb.row(InlineKeyboardButton(text=SHOW_SECRET_KEYS_IKB_MESSAGE, callback_data=SHOW_SECRET_KEYS_DATA))
    ikb.row(InlineKeyboardButton(text=DELETE_SECRET_KEYS_IKB_MESSAGE, callback_data=DELETE_SECRET_KEYS_DATA))
    ikb.row(InlineKeyboardButton(text=ALERT_FOR_USERS_IKB_MESSAGE, callback_data=ALERT_FOR_USERS_DATA))

    return ikb
