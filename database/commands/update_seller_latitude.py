from database import SellerGeodata


async def update_seller_latitude(seller_id: int, latitude: str):
    """
    :param seller_id: Телеграм user id.
    :param latitude: Широта.
    """

    await SellerGeodata.update.values(latitude=latitude).where(SellerGeodata.seller_id == seller_id).gino.scalar()
