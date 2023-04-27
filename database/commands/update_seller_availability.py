from database import SellerInfo


async def update_seller_availability(seller_id: int, availability: int) -> None:
    """
    :param seller_id: Телеграм user id.
    :param availability: 0, если у продавца закончился квас и 1, если он есть.
    """

    await SellerInfo.update.values(availability=availability).where(SellerInfo.seller_id == seller_id).gino.scalar()
