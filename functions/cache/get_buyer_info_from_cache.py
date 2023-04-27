from typing import Union

from loader import buyer_info_cache

from database import get_buyer_info


async def get_buyer_info_from_cache(buyer_id: int) -> Union[dict, None]:
    """
    :param buyer_id: Телеграм user id.
    :return: Словарь с информацией о покупателе, если он есть, иначе - None.
    """

    if buyer_id in buyer_info_cache:
        buyer_info = buyer_info_cache[buyer_id]
    else:
        buyer_info = await get_buyer_info(buyer_id)
        if buyer_info is not None:
            buyer_info_cache[buyer_id] = buyer_info

    return buyer_info
