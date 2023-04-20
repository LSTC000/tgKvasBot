from data.config import ROW_WIDTH

from data.callbacks import BUYER_CHOICE_BRAND_DATA, FIND_NEAREST_SELLER_DATA, CANCEL_TO_MAIN_MENU_DATA

from data.messages import (
    BUYER_CHOICE_BRAND_IKB_MESSAGE,
    FIND_NEAREST_SELLER_IKB_MESSAGE,
    CANCEL_TO_MAIN_MENU_IKB_MESSAGE
)

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton


def buyer_menu_ikb() -> InlineKeyboardMarkup:
    """
    :return: Клавиатура меню покупателя.
    """

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(InlineKeyboardButton(text=BUYER_CHOICE_BRAND_IKB_MESSAGE, callback_data=BUYER_CHOICE_BRAND_DATA))
    ikb.row(InlineKeyboardButton(text=FIND_NEAREST_SELLER_IKB_MESSAGE, callback_data=FIND_NEAREST_SELLER_DATA))
    ikb.row(InlineKeyboardButton(text=CANCEL_TO_MAIN_MENU_IKB_MESSAGE, callback_data=CANCEL_TO_MAIN_MENU_DATA))

    return ikb
