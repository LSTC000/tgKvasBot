from data.config import ROW_WIDTH

from data.callbacks import (
    SELLER_CHANGE_CITY_DATA,
    SELLER_CHANGE_BRAND_DATA,
    DELETE_SELLER_DATA,
    CANCEL_TO_SELLER_MENU_DATA
)

from data.messages import (
    SELLER_CHANGE_CITY_IKB_MESSAGE,
    SELLER_CHANGE_BRAND_IKB_MESSAGE,
    DELETE_SELLER_IKB_MESSAGE,
    CANCEL_TO_SELLER_MENU_IKB_MESSAGE
)

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton


def seller_settings_menu_ikb() -> InlineKeyboardMarkup:
    """
    :return: Клавиатура настроек продавца.
    """

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(
        InlineKeyboardButton(text=SELLER_CHANGE_CITY_IKB_MESSAGE, callback_data=SELLER_CHANGE_CITY_DATA),
        InlineKeyboardButton(text=SELLER_CHANGE_BRAND_IKB_MESSAGE, callback_data=SELLER_CHANGE_BRAND_DATA)
    )
    ikb.row(InlineKeyboardButton(text=DELETE_SELLER_IKB_MESSAGE, callback_data=DELETE_SELLER_DATA))
    ikb.row(InlineKeyboardButton(text=CANCEL_TO_SELLER_MENU_IKB_MESSAGE, callback_data=CANCEL_TO_SELLER_MENU_DATA))

    return ikb
