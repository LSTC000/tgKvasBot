from data.config import ROW_WIDTH

from data.callbacks import FIND_NEAREST_SELLER_DATA, SELLER_MENU_DATA, BUYER_SETTINGS_MENU_DATA

from data.messages import FIND_NEAREST_SELLER_IKB_MESSAGE, SELLER_MENU_IKB_MESSAGE, SETTINGS_MENU_IKB_MESSAGE

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton


def main_menu_ikb() -> InlineKeyboardMarkup:
    """
    :return: Клавиатура главного меню.
    """

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(InlineKeyboardButton(text=FIND_NEAREST_SELLER_IKB_MESSAGE, callback_data=FIND_NEAREST_SELLER_DATA))
    ikb.row(InlineKeyboardButton(text=SELLER_MENU_IKB_MESSAGE, callback_data=SELLER_MENU_DATA))
    ikb.row(InlineKeyboardButton(text=SETTINGS_MENU_IKB_MESSAGE, callback_data=BUYER_SETTINGS_MENU_DATA))

    return ikb
