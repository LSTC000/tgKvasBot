from typing import List

from loader import cities_cache

from data.cache import CITIES_CACHE_KEY

from database import get_cities


async def get_cities_from_cache() -> List[str]:
    """
    :return: Список доступных для выбора городов.
    """

    if CITIES_CACHE_KEY in cities_cache:
        cities = cities_cache[CITIES_CACHE_KEY]
    else:
        cities = await get_cities()
        cities = [city[0] for city in cities]
        cities_cache[CITIES_CACHE_KEY] = cities

    return cities
