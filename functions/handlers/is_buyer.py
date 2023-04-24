from database import get_buyer


async def is_buyer(buyer_id: int) -> bool:
    """
    :param buyer_id: Телеграм user id.
    :return: True - если пальзователь зарегистрирован, иначе - False.
    """

    return True if await get_buyer(buyer_id) is not None else False
