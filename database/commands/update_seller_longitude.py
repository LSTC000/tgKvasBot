from database import SellerGeodata


async def update_seller_longitude(seller_id: int, longitude: float):
    """
    :param seller_id: Телеграм user id.
    :param longitude: Долгота.
    """

    await SellerGeodata.update.values(longitude=longitude).where(SellerGeodata.seller_id == seller_id).gino.scalar()
