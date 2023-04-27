from typing import Union

from functions import get_seller_info_from_cache


async def get_seller_geodata(seller_id: int) -> Union[dict, None]:
    '''
    :param seller_id: Телеграм user id.
    :return: Словарь с геоданными, если они есть. Иначе - None.
    '''

    seller_info = await get_seller_info_from_cache(seller_id)

    return {
        'city': seller_info['city'],
        'brand': seller_info['brand'],
        'latitude': seller_info['latitude'],
        'longitude': seller_info['longitude']
    } if seller_info['latitude'] else None
