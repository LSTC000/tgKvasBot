from functions import get_seller_info_from_cache


async def is_seller(seller_id: int) -> bool:
    """
    :param seller_id: Телеграм user id.
    :return: True - если продавец зарегистрирован, иначе - False.
    """

    return True if await get_seller_info_from_cache(seller_id) is not None else False
