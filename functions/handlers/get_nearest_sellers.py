from typing import Union

from data.redis import NEAREST_SELLERS_REDIS_KEY

from database import get_sellers_info

from functions import get_buyer_info_from_cache

from geopy.distance import distance

from aiogram.dispatcher.storage import FSMContext


async def get_nearest_sellers(
        buyer_id: int,
        latitude: float,
        longitude: float,
        state: FSMContext
) -> Union[list, None]:
    """
    :param buyer_id: Телеграм user id.
    :param latitude: Широта.
    :param longitude: Долгота.
    :param state: FSMContext.
    :return: Список с информацией о ближайших продавцах, если ближайших продавцов нет - None.
    """

    buyer = await get_buyer_info_from_cache(buyer_id)

    city = buyer['city']
    brand = buyer['brand']

    sellers_info = await get_sellers_info(city, brand)

    if sellers_info:
        distances = []
        for seller_key in sellers_info.keys():
            dist = distance(
                (latitude, longitude),
                (sellers_info[seller_key]['latitude'], sellers_info[seller_key]['longitude'])
            ).km
            distances.append((sellers_info[seller_key], dist))

        distances.sort(key=lambda x: x[1])

        async with state.proxy() as data:
            data[NEAREST_SELLERS_REDIS_KEY] = distances

        return distances

    return None
