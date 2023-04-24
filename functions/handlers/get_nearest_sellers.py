from typing import Union

from data.redis import NEAREST_SELLERS_REDIS_KEY

from database import get_buyer, get_sellers_data

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

    buyer = await get_buyer(buyer_id)

    city = buyer['city']
    brand = buyer['brand']

    sellers_data = await get_sellers_data(city, brand)

    if sellers_data:
        distances = []
        for seller_key in sellers_data:
            dist = distance(
                (latitude, longitude),
                (sellers_data[seller_key]['latitude'], sellers_data[seller_key]['longitude'])
            ).km
            distances.append((sellers_data[seller_key], dist))

        distances.sort(key=lambda x: x[1])

        async with state.proxy() as data:
            data[NEAREST_SELLERS_REDIS_KEY] = distances

        return distances

    return None
