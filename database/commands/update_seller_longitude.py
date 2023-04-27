from database import SellerInfo


async def update_seller_longitude(seller_id: int, longitude: float) -> None:
    """
    :param seller_id: Телеграм user id.
    :param longitude: Долгота.
    """

    await SellerInfo.update.values(longitude=longitude).where(SellerInfo.seller_id == seller_id).gino.scalar()
