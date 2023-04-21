from database import SellerInfo


async def get_seller_info(seller_id: int) -> dict:
    """
    :param seller_id: Телеграм user id.
    :return: Список с данными продавца.
    """

    seller_info_list = await SellerInfo.query.where(SellerInfo.seller_id == seller_id).gino.all()
    seller_info_values = [seller_info.__dict__ for seller_info in seller_info_list]
    return seller_info_values[0]['__values__']
