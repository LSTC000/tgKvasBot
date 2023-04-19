from database import get_buyer


async def is_buyer(user_id: int) -> bool:
    """
    :param user_id: Телеграм user id.
    :return: True - если пальзователь зарегистрирован, иначе - False.
    """

    return True if await get_buyer(user_id) else False
