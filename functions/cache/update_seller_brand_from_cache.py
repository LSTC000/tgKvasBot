from loader import seller_info_cache

from database import update_seller_brand


async def update_seller_brand_from_cache(seller_id: int, brand: str) -> None:
    """
    :param seller_id: Телеграм user id.
    :param brand: Новый выбранный бренд продавца.
    """

    await update_seller_brand(seller_id, brand)

    if seller_id in seller_info_cache:
        seller_info_cache[seller_id]['brand'] = brand
