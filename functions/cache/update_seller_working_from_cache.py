from loader import seller_info_cache

from database import update_seller_working


async def update_seller_working_from_cache(seller_id: int, working: int) -> None:
    """
    :param seller_id: Телеграм user id.
    :param working: 0, если продавец не работает и 1, если работает.
    """

    await update_seller_working(seller_id, working)

    if seller_id in seller_info_cache:
        seller_info_cache[seller_id]['working'] = working
