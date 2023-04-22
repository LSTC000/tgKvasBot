from database import SellerGeodata


async def update_seller_address_url(seller_id: int, address_url: str):
    """
    :param seller_id: Телеграм user id.
    :param address_url: URL адрес продавца.
    """

    await SellerGeodata.update.values(address_url=address_url).where(SellerGeodata.seller_id == seller_id).gino.scalar()
