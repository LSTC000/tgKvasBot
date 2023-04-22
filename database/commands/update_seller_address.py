from database import SellerGeodata


async def update_seller_address(seller_id: int, address: str):
    """
    :param seller_id: Телеграм user id.
    :param address: Адрес продавца.
    """

    await SellerGeodata.update.values(address=address).where(SellerGeodata.seller_id == seller_id).gino.scalar()
