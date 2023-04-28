from data.config import ROW_WIDTH

from data.callbacks import CREATE_SECRET_KEY_DATA, SHOW_AVAILABLE_SECRET_KEYS_DATA

from data.messages import CREATE_SECRET_KEY_IKB_MESSAGE, SHOW_AVAILABLE_SECRET_KEYS_IKB_MESSAGE

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_menu_ikb() -> InlineKeyboardMarkup:
    """
    :return: Клавиатура меню администратора.
    """

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(InlineKeyboardButton(
        text=CREATE_SECRET_KEY_IKB_MESSAGE,
        callback_data=CREATE_SECRET_KEY_DATA)
    )
    ikb.row(InlineKeyboardButton(
        text=SHOW_AVAILABLE_SECRET_KEYS_IKB_MESSAGE,
        callback_data=SHOW_AVAILABLE_SECRET_KEYS_DATA)
    )

    return ikb
