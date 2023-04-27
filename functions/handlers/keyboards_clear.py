from data.redis import (
    LAST_IKB_REDIS_KEY,
    LAST_RKB_REDIS_KEY,
    LAST_SELLER_INFO_MESSAGE_REDIS_KEY,
    LAST_SEND_LOCATION_IKB_REDIS_KEY
)

from loader import bot

from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound


async def keyboards_clear(user_id: int, state: FSMContext) -> None:
    '''
    :param user_id: Телеграм user_id.
    :param state: FSMContext.
    '''

    async with state.proxy() as data:
        if LAST_IKB_REDIS_KEY in data:
            try:
                await bot.delete_message(chat_id=user_id, message_id=data[LAST_IKB_REDIS_KEY])
            except MessageToDeleteNotFound:
                pass
        if LAST_RKB_REDIS_KEY in data:
            try:
                await bot.delete_message(chat_id=user_id, message_id=data[LAST_RKB_REDIS_KEY])
            except MessageToDeleteNotFound:
                pass
        if LAST_SELLER_INFO_MESSAGE_REDIS_KEY in data:
            try:
                await bot.delete_message(chat_id=user_id, message_id=data[LAST_SELLER_INFO_MESSAGE_REDIS_KEY])
            except MessageToDeleteNotFound:
                pass
        if LAST_SEND_LOCATION_IKB_REDIS_KEY in data:
            try:
                await bot.delete_message(chat_id=user_id, message_id=data[LAST_SEND_LOCATION_IKB_REDIS_KEY])
            except MessageToDeleteNotFound:
                pass
