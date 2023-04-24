from typing import Union

from database import Buyer


async def get_buyer(buyer_id: int) -> Union[dict, None]:
    """
    :param buyer_id: Телеграм user id.
    :return: Словарь с данными пользователя, если пользователя нет - None.
    """

    buyer_info_list = await Buyer.query.where(Buyer.buyer_id == buyer_id).gino.all()

    if buyer_info_list:
        buyer_info_values = [_.__dict__ for _ in buyer_info_list]
        return buyer_info_values[0]['__values__']

    return None
