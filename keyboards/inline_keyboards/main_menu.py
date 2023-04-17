from data.config import ROW_WIDTH

from data.callbacks import BUYER_MENU_DATA, SELLER_MENU_DATA

from data.messages import BUYER_MENU_IKB_MESSAGE, SELLER_MENU_IKB_MESSAGE

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton


def main_menu_ikb() -> InlineKeyboardMarkup:
    """
    :return: Клавиатура главного меню.
    """

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(InlineKeyboardButton(text=BUYER_MENU_IKB_MESSAGE, callback_data=BUYER_MENU_DATA))
    ikb.row(InlineKeyboardButton(text=SELLER_MENU_IKB_MESSAGE, callback_data=SELLER_MENU_DATA))

    return ikb
