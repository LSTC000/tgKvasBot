from loader import buyer_info_cache

from database import update_buyer_city


async def update_buyer_city_from_cache(buyer_id: int, city: str):
    """
    :param buyer_id: Телеграм user id.
    :param city: Новый выбранный город покупателя.
    """

    await update_buyer_city(buyer_id, city)

    if buyer_id in buyer_info_cache:
        buyer_info_cache[buyer_id]['city'] = city
