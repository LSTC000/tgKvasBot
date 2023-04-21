from database import SellerAddress


async def delete_seller_address(seller_id: int):
    """
    :param seller_id: Телеграм user id.
    """

    return await SellerAddress.delete.where(SellerAddress.seller_id == seller_id).gino.scalar()
