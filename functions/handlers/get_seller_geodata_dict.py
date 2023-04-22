from typing import Union

from database import get_seller_geodata


async def get_seller_geodata_dict(seller_id: int) -> Union[dict, None]:
    '''
    :param seller_id: Телеграм user id.
    :return: Словарь с геоданными, если они есть. Иначе - None.
    '''

    seller_geodata = await get_seller_geodata(seller_id)

    return {
        'city': seller_geodata['city'],
        'brand': seller_geodata['brand'],
        'latitude': seller_geodata['latitude'],
        'longitude': seller_geodata['longitude'],
        'address': seller_geodata['address'],
        'address_url': seller_geodata['address_url']
    } if seller_geodata['latitude'] else None
