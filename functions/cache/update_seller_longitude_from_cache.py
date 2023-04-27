from loader import seller_info_cache

from database import update_seller_longitude


async def update_seller_longitude_from_cache(seller_id: int, longitude: float):
    """
    :param seller_id: Телеграм user id.
    :param longitude: Долгота.
    """

    await update_seller_longitude(seller_id, longitude)

    if seller_id in seller_info_cache:
        seller_info_cache[seller_id]['longitude'] = longitude
