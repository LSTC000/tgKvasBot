from database import SellerInfo


async def update_seller_pause(seller_id: int, pause: int):
    """
    :param seller_id: Телеграм user id.
    :param pause: 0, если продавец не на перерыве и 1, если на перерыве.
    """

    await SellerInfo.update.values(pause=pause).where(SellerInfo.seller_id == seller_id).gino.scalar()
