from loader import seller_info_cache

from database import update_seller_pause


async def update_seller_pause_from_cache(seller_id: int, pause: int) -> None:
    """
    :param seller_id: Телеграм user id.
    :param pause: 0, если продавец не на перерыве и 1, если на перерыве.
    """

    await update_seller_pause(seller_id, pause)

    if seller_id in seller_info_cache:
        seller_info_cache[seller_id]['pause'] = pause
