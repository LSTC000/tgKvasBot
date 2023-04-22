from data.config import ROW_WIDTH

from data.callbacks import SELLER_MENU_DATA, SETTINGS_MAIN_MENU_DATA

from data.messages import SELLER_MENU_IKB_MESSAGE, SETTINGS_MAIN_MENU_IKB_MESSAGE

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_ikb() -> InlineKeyboardMarkup:
    """
    :return: Клавиатура главного меню.
    """

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(
        InlineKeyboardButton(text=SELLER_MENU_IKB_MESSAGE, callback_data=SELLER_MENU_DATA),
        InlineKeyboardButton(text=SETTINGS_MAIN_MENU_IKB_MESSAGE, callback_data=SETTINGS_MAIN_MENU_DATA)
    )

    return ikb
