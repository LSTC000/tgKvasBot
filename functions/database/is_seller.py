from database import get_seller


async def is_seller(seller_id: int) -> bool:
    """
    :param seller_id: Телеграм user id.
    :return: True - если продавец зарегистрирован, иначе - False.
    """

    return True if await get_seller(seller_id) else False
