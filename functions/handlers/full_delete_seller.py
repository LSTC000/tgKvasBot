from loader import seller_cache

from database import delete_seller, delete_seller_info, delete_seller_address


async def full_delete_seller(seller_id: int):
    """
    :param seller_id: Телеграм user id.
    """

    # Удаляем продавца из БД.
    await delete_seller(seller_id)
    await delete_seller_info(seller_id)
    await delete_seller_address(seller_id)

    # Если продавец ещё в кэше, то удаляем его оттуда.
    if seller_id in seller_cache:
        seller_cache.pop(seller_id)
