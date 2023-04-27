from database import SellerInfo


async def update_seller_city(seller_id: int, city: str) -> None:
    """
    :param seller_id: Телеграм user id.
    :param city: Новый выбранный город продавца.
    """

    await SellerInfo.update.values(city=city).where(SellerInfo.seller_id == seller_id).gino.scalar()
