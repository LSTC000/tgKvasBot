from database import SellerInfo


async def delete_seller_info(seller_id: int) -> None:
    """
    :param seller_id: Телеграм user id.
    """

    return await SellerInfo.delete.where(SellerInfo.seller_id == seller_id).gino.scalar()
