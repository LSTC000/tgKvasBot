from data.config import ROW_WIDTH

from data.callbacks import BUYER_CHOICE_CITY_DATA, SUPPORT_BUYER_REGISTER_DATA

from data.messages import BUYER_CHOICE_CITY_IKB_MESSAGE, SUPPORT_BUYER_REGISTER_IKB_MESSAGE

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton


def buyer_register_menu_ikb() -> InlineKeyboardMarkup:
    """
    :return: Клавиатура для регистрации покупателя.
    """

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(InlineKeyboardButton(text=BUYER_CHOICE_CITY_IKB_MESSAGE, callback_data=BUYER_CHOICE_CITY_DATA))
    ikb.row(InlineKeyboardButton(text=SUPPORT_BUYER_REGISTER_IKB_MESSAGE, callback_data=SUPPORT_BUYER_REGISTER_DATA))

    return ikb
