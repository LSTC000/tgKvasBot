from database import Seller


async def get_seller(seller_id: int) -> list:
    """
    :param seller_id: Телеграм user id.
    :return: Id продавца.
    """

    return await Seller.query.where(Seller.seller_id == seller_id).gino.all()
