from data.config import RESIZE_KEYBOARD

from data.messages import SELLER_UPDATE_GEODATA_RKB_MESSAGE

from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton


def seller_update_geodata_menu_rkb() -> ReplyKeyboardMarkup:
    """
    :return: Клавиатура обновления геолокации.
    """

    ikb = ReplyKeyboardMarkup(resize_keyboard=RESIZE_KEYBOARD)

    ikb.row(KeyboardButton(text=SELLER_UPDATE_GEODATA_RKB_MESSAGE, request_location=True))

    return ikb
