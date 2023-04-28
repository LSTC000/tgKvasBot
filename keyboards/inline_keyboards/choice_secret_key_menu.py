from data.config import ROW_WIDTH

from data.callbacks import CANCEL_TO_LAST_MENU_DATA

from data.messages import CANCEL_TO_LAST_MENU_IKB_MESSAGE

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def choice_secret_key_menu_ikb(secret_keys: list) -> InlineKeyboardMarkup:
    """
    :param secret_keys: Список с секретными ключами.
    :return: Клавиатура для выбора секретного ключа.
    """

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    for secret_key in secret_keys:
        ikb.add(InlineKeyboardButton(text=secret_key, callback_data=secret_key))

    ikb.add(InlineKeyboardButton(text=CANCEL_TO_LAST_MENU_IKB_MESSAGE, callback_data=CANCEL_TO_LAST_MENU_DATA))

    return ikb
