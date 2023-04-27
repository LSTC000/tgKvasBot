from typing import Union

from loader import seller_info_cache

from database import get_seller_info


async def get_seller_info_from_cache(seller_id: int) -> Union[dict, None]:
    """
    :param seller_id: Телеграм user id.
    :return: Словарь с информацией о продавце, если он есть, иначе - None.
    """

    if seller_id in seller_info_cache:
        seller_info = seller_info_cache[seller_id]
    else:
        seller_info = await get_seller_info(seller_id)
        if seller_info is not None:
            seller_info_cache[seller_id] = seller_info

    return seller_info
