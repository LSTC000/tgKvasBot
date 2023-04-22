from loader import bot

from data.redis import LAST_RKB_REDIS_KEY

from aiogram.dispatcher.storage import FSMContext


async def reload_rkb(
        user_id: int,
        text: str,
        new_rkb,
        state: FSMContext
) -> None:
    '''
    :param user_id: Телеграм user_id.
    :param text: Текст для новой rkb клавиатуры.
    :param new_rkb: Новая rkb клавиатура пользователя.
    :param state: FSMContext.
    :return: None
    '''

    async with state.proxy() as data:
        # Вызываем новую rkb клавиатуру.
        msg = await bot.send_message(chat_id=user_id, text=text, reply_markup=new_rkb())

        # Добавляем новую rkb клавиатуру в redis.
        data[LAST_RKB_REDIS_KEY] = msg.message_id
