from database import SellerInfo


async def update_seller_working(seller_id: int, working: int):
    """
    :param seller_id: Телеграм user id.
    :param working: 0, если продавец не работает и 1, если работает.
    """

    await SellerInfo.update.values(working=working).where(SellerInfo.seller_id == seller_id).gino.scalar()
