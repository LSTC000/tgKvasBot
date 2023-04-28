from loader import seller_info_cache

from database import update_seller_availability


async def update_seller_availability_from_cache(seller_id: int, availability: int) -> None:
    """
    :param seller_id: Телеграм user id.
    :param availability: 0, если у продавца закончился квас и 1, если он есть.
    """

    await update_seller_availability(seller_id, availability)

    if seller_id in seller_info_cache:
        seller_info_cache[seller_id]['availability'] = availability
