from data.config import ROW_WIDTH

from data.callbacks import (
    SELLER_CHOICE_CITY_DATA,
    SELLER_CHOICE_BRAND_DATA,
    CONFIRM_SELLER_REGISTER_DATA,
    CANCEL_TO_MAIN_MENU_DATA,
    SUPPORT_SELLER_REGISTER_DATA
)

from data.messages import (
    SELLER_CHOICE_CITY_IKB_MESSAGE,
    SELLER_CHOICE_BRAND_IKB_MESSAGE,
    CONFIRM_SELLER_REGISTER_IKB_MESSAGE,
    CANCEL_TO_MAIN_MENU_IKB_MESSAGE,
    SUPPORT_SELLER_REGISTER_IKB_MESSAGE
)

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton


def seller_register_menu_ikb() -> InlineKeyboardMarkup:
    """
    :return: Клавиатура для регистрации продавца продавца.
    """

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(InlineKeyboardButton(text=SELLER_CHOICE_CITY_IKB_MESSAGE, callback_data=SELLER_CHOICE_CITY_DATA))
    ikb.row(InlineKeyboardButton(text=SELLER_CHOICE_BRAND_IKB_MESSAGE, callback_data=SELLER_CHOICE_BRAND_DATA))
    ikb.row(InlineKeyboardButton(text=CONFIRM_SELLER_REGISTER_IKB_MESSAGE, callback_data=CONFIRM_SELLER_REGISTER_DATA))
    ikb.row(InlineKeyboardButton(text=CANCEL_TO_MAIN_MENU_IKB_MESSAGE, callback_data=CANCEL_TO_MAIN_MENU_DATA))
    ikb.row(InlineKeyboardButton(text=SUPPORT_SELLER_REGISTER_IKB_MESSAGE, callback_data=SUPPORT_SELLER_REGISTER_DATA))

    return ikb
