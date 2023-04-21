from data.config import ROW_WIDTH

from data.callbacks import SETTINGS_SELLER_MENU_DATA, CANCEL_TO_MAIN_MENU_DATA

from data.messages import SETTINGS_SELLER_MENU_IKB_MESSAGE, CANCEL_TO_MAIN_MENU_IKB_MESSAGE

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton


def seller_menu_ikb(
    availability_message: str,
    working_message: str,
    pause_message: str,
    availability_data: str,
    working_data: str,
    pause_data: str
) -> InlineKeyboardMarkup:
    """
    :param availability_message: AVAILABILITY_IKB_MESSAGE или UNAVAILABILITY_IKB_MESSAGE в
        data/messages/keyboards/keyboards_messages.
    :param working_message: START_WORKING_IKB_MESSAGE или STOP_WORKING_IKB_MESSAGE в
        data/messages/keyboards/keyboards_messages.
    :param pause_message: START_PAUSE_IKB_MESSAGE или STOP_PAUSE_IKB_MESSAGE в
        data/messages/keyboards/keyboards_messages.
    :param availability_data: AVAILABILITY_DATA или UNAVAILABILITY_DATA в data/callbacks/callbacks_data.
    :param working_data: START_WORKING_DATA или STOP_WORKING_DATA в data/callbacks/callbacks_data.
    :param pause_data: START_PAUSE_DATA или STOP_PAUSE_DATA в data/callbacks/callbacks_data.
    :return: Клавиатура меню продавца.
    """

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(InlineKeyboardButton(text=availability_message, callback_data=availability_data))
    ikb.row(InlineKeyboardButton(text=pause_message, callback_data=pause_data))
    ikb.row(InlineKeyboardButton(text=working_message, callback_data=working_data))
    ikb.row(
        InlineKeyboardButton(text=CANCEL_TO_MAIN_MENU_IKB_MESSAGE, callback_data=CANCEL_TO_MAIN_MENU_DATA),
        InlineKeyboardButton(text=SETTINGS_SELLER_MENU_IKB_MESSAGE, callback_data=SETTINGS_SELLER_MENU_DATA)
    )

    return ikb
