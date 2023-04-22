from data.config import RESIZE_KEYBOARD

from data.messages import FIND_NEAREST_SELLER_RKB_MESSAGE

from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton


def buyer_find_nearest_seller_menu_rkb() -> ReplyKeyboardMarkup:
    """
    :return: Клавиатура нахождения ближайшего продавца.
    """

    ikb = ReplyKeyboardMarkup(resize_keyboard=RESIZE_KEYBOARD)

    ikb.row(KeyboardButton(text=FIND_NEAREST_SELLER_RKB_MESSAGE, request_location=True))

    return ikb
