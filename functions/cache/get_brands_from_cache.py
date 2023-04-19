from typing import List

from loader import brands_cache

from data.cache import BRANDS_CACHE_KEY

from database import get_brands


async def get_brands_from_cache() -> List[str]:
    """
    :return: Список доступных для выбора брендов.
    """

    if BRANDS_CACHE_KEY in brands_cache:
        brands = brands_cache[BRANDS_CACHE_KEY]
    else:
        brands = await get_brands()
        brands = [brand[0] for brand in brands]
        brands_cache[BRANDS_CACHE_KEY] = brands

    return brands
