from database import Seller


async def delete_seller(seller_id: int):
    """
    :param seller_id: Телеграм user id.
    """

    return await Seller.delete.where(Seller.seller_id == seller_id).gino.scalar()
