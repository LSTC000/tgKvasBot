from database import Buyer


async def update_buyer(buyer_id: int, city: str):
    """
    :param buyer_id: Телеграм user id.
    :param city: Новый выбранный город пользователя.
    """

    await Buyer.update.values(city=city).where(Buyer.buyer_id == buyer_id).gino.scalar()
