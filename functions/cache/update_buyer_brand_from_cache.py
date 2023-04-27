from typing import Union

from loader import buyer_info_cache

from database import update_buyer_brand


async def update_buyer_brand_from_cache(buyer_id: int, brand: Union[str, None]):
    """
    :param buyer_id: Телеграм user id.
    :param brand: Новый выбранный бренд покупателя.
    """

    await update_buyer_brand(buyer_id, brand)

    if buyer_id in buyer_info_cache:
        buyer_info_cache[buyer_id]['brand'] = brand
