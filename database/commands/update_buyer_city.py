from database import BuyerInfo


async def update_buyer_city(buyer_id: int, city: str) -> None:
    """
    :param buyer_id: Телеграм user id.
    :param city: Новый выбранный город покупателя.
    """

    await BuyerInfo.update.values(city=city).where(BuyerInfo.buyer_id == buyer_id).gino.scalar()
