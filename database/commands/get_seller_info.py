from typing import Union

from database import SellerInfo


async def get_seller_info(seller_id: int) -> Union[dict, None]:
    """
    :param seller_id: Телеграм user id.
    :return: Словарь с информацией о продавце, если продавца нет - None.
    """

    seller_info_list = await SellerInfo.query.where(SellerInfo.seller_id == seller_id).gino.all()

    if seller_info_list:
        seller_info_values = [_.__dict__ for _ in seller_info_list]
        seller_info_values = seller_info_values[0]['__values__'][0]
        return {
                    'city': seller_info_values[2],
                    'brand': seller_info_values[3],
                    'availability': seller_info_values[4],
                    'working': seller_info_values[5],
                    'pause': seller_info_values[6],
                    'latitude': seller_info_values[7],
                    'longitude': seller_info_values[8]
                }

    return None
