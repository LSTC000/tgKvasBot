from database import Buyer


async def update_buyer_city(buyer_id: int, city: str):
    """
    :param buyer_id: Телеграм user id.
    :param city: Новый выбранный город покупателя.
    """

    await Buyer.update.values(city=city).where(Buyer.buyer_id == buyer_id).gino.scalar()
