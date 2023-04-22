from database import SellerGeodata


async def update_seller_brand(seller_id: int, brand: str):
    """
    :param seller_id: Телеграм user id.
    :param brand: Новый выбранный бренд продавца.
    """

    await SellerGeodata.update.values(brand=brand).where(SellerGeodata.seller_id == seller_id).gino.scalar()
