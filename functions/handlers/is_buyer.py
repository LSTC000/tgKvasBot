from functions import get_buyer_info_from_cache


async def is_buyer(buyer_id: int) -> bool:
    """
    :param buyer_id: Телеграм user id.
    :return: True - если пальзователь зарегистрирован, иначе - False.
    """

    return True if await get_buyer_info_from_cache(buyer_id) is not None else False
