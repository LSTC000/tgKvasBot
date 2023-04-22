from database import SellerGeodata


async def update_seller_city(seller_id: int, city: str):
    """
    :param seller_id: Телеграм user id.
    :param city: Новый выбранный город продавца.
    """

    await SellerGeodata.update.values(city=city).where(SellerGeodata.seller_id == seller_id).gino.scalar()
