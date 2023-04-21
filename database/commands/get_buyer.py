from database import Buyer


async def get_buyer(buyer_id: int) -> list:
    """
    :param buyer_id: Телеграм user id.
    :return: Список с данными пользователя.
    """

    return await Buyer.query.where(Buyer.buyer_id == buyer_id).gino.all()
