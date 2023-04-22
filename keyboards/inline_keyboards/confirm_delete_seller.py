from data.config import ROW_WIDTH

from data.callbacks import CONFIRM_DELETE_SELLER_DATA, CANCEL_DELETE_SELLER_DATA

from data.messages import CONFIRM_DELETE_SELLER_IKB_MESSAGE, CANCEL_DELETE_SELLER_IKB_MESSAGE

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def confirm_delete_seller_ikb() -> InlineKeyboardMarkup:
    """
    :return: Клавиатура для подтверждения удаления покупателя.
    """

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(InlineKeyboardButton(text=CONFIRM_DELETE_SELLER_IKB_MESSAGE, callback_data=CONFIRM_DELETE_SELLER_DATA))
    ikb.row(InlineKeyboardButton(text=CANCEL_DELETE_SELLER_IKB_MESSAGE, callback_data=CANCEL_DELETE_SELLER_DATA))

    return ikb
