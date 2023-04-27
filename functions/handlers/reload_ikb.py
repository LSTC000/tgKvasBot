from data.redis import LAST_IKB_REDIS_KEY

from functions.handlers import keyboards_clear

from loader import bot

from aiogram.dispatcher.storage import FSMContext


async def reload_ikb(
        user_id: int,
        text: str,
        new_ikb,
        state: FSMContext,
        ikb_params: dict = None
) -> None:
    '''
    :param user_id: Телеграм user_id.
    :param text: Текст для новой ikb клавиатуры.
    :param new_ikb: Новая ikb клавиатура пользователя.
    :param state: FSMContext.
    :param ikb_params: Параметры для новой ikb клавиатуры пользователя. По умолчанию: None.
    :return: None
    '''

    # Удаляем все старые клавиатуры.
    await keyboards_clear(user_id, state)

    async with state.proxy() as data:
        # Вызываем новую ikb клавиатуру.
        msg = await bot.send_message(
            chat_id=user_id,
            text=text,
            reply_markup=new_ikb(**ikb_params) if ikb_params is not None else new_ikb()
        )

        # Добавляем новую ikb клавиатуру в redis.
        data[LAST_IKB_REDIS_KEY] = msg.message_id
