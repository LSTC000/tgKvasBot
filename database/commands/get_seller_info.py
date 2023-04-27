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
        seller_info_values = seller_info_values[0]['__values__']
        return {
                    'city': seller_info_values['city'],
                    'brand': seller_info_values['brand'],
                    'availability': seller_info_values['availability'],
                    'working': seller_info_values['working'],
                    'pause': seller_info_values['pause'],
                    'latitude': seller_info_values['latitude'],
                    'longitude': seller_info_values['longitude']
                }

    return None
