from database import SellerAddress


async def update_seller_brand(seller_id: int, brand: str):
    """
    :param seller_id: Телеграм user id.
    :param brand: Новый выбранный бренд продавца.
    """

    await SellerAddress.update.values(brand=brand).where(SellerAddress.seller_id == seller_id).gino.scalar()
