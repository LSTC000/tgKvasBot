from database import SellerAddress


async def update_seller_city(seller_id: int, city: str):
    """
    :param seller_id: Телеграм user id.
    :param city: Новый выбранный город продавца.
    """

    await SellerAddress.update.values(city=city).where(SellerAddress.seller_id == seller_id).gino.scalar()
