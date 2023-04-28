from loader import seller_info_cache

from database import update_seller_city


async def update_seller_city_from_cache(seller_id: int, city: str) -> None:
    """
    :param seller_id: Телеграм user id.
    :param city: Новый выбранный город продавца.
    """

    await update_seller_city(seller_id, city)

    if seller_id in seller_info_cache:
        seller_info_cache[seller_id]['city'] = city
