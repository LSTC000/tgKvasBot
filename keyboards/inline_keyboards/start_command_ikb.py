from data.config import ROW_WIDTH

from data.callbacks import START_COMMAND_DATA

from data.messages import START_COMMAND_IKB_MESSAGE

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton


def start_command_ikb() -> InlineKeyboardMarkup:
    """
    :return: Клавиатура для старта бота.
    """

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(InlineKeyboardButton(text=START_COMMAND_IKB_MESSAGE, callback_data=START_COMMAND_DATA))

    return ikb
