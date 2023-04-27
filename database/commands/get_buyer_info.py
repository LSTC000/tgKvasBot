from typing import Union

from database import BuyerInfo


async def get_buyer_info(buyer_id: int) -> Union[dict, None]:
    """
    :param buyer_id: Телеграм user id.
    :return: Словарь с данными пользователя, если пользователя нет - None.
    """

    buyer_info_list = await BuyerInfo.query.where(BuyerInfo.buyer_id == buyer_id).gino.all()

    if buyer_info_list:
        buyer_info_values = [_.__dict__ for _ in buyer_info_list]
        buyer_info_values = buyer_info_values[0]['__values__']
        return {
            'city': buyer_info_values['city'],
            'brand': buyer_info_values['brand']
        }

    return None
