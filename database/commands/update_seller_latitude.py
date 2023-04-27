from database import SellerInfo


async def update_seller_latitude(seller_id: int, latitude: float) -> None:
    """
    :param seller_id: Телеграм user id.
    :param latitude: Широта.
    """

    await SellerInfo.update.values(latitude=latitude).where(SellerInfo.seller_id == seller_id).gino.scalar()
