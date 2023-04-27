from database import SellerInfo


async def update_seller_brand(seller_id: int, brand: str) -> None:
    """
    :param seller_id: Телеграм user id.
    :param brand: Новый выбранный бренд продавца.
    """

    await SellerInfo.update.values(brand=brand).where(SellerInfo.seller_id == seller_id).gino.scalar()
