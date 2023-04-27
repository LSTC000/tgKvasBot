from loader import seller_info_cache

from database import update_seller_latitude


async def update_seller_latitude_from_cache(seller_id: int, latitude: float):
    """
    :param seller_id: Телеграм user id.
    :param latitude: Широта.
    """

    await update_seller_latitude(seller_id, latitude)

    if seller_id in seller_info_cache:
        seller_info_cache[seller_id]['latitude'] = latitude
