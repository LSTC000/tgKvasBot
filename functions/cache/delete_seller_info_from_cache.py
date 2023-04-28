from loader import seller_info_cache

from database import delete_seller_info, delete_secret_key


async def delete_seller_info_from_cache(seller_id: int) -> None:
    """
    :param seller_id: Телеграм user id.
    """

    # Удаляем продавца из БД.
    await delete_seller_info(seller_id)

    # Удаляем cекретный ключ продавца из БД.
    await delete_secret_key(seller_id)

    # Если продавец в кэше, то удаляем его оттуда.
    if seller_id in seller_info_cache:
        seller_info_cache.pop(seller_id)
