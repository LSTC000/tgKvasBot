from typing import List

from database import Buyer


async def get_buyer(user_id: int) -> List:
    """
    :param user_id: Телеграм user id.
    :return: Список с данными пользователя.
    """

    return await Buyer.query.where(Buyer.buyer_id == user_id).gino.all()
