from typing import Union

from database import SellerInfo


async def get_sellers_info(city: str, brand: Union[str, None]) -> dict:
    """
    :param city: Выбранный город покупателя.
    :param brand: Выбранный бренд покупателя или None - если покупателя интересует любой бренд.
    :return: Словарь с информацией о всех подходящих продавцах.
    """

    if brand is not None:
        sellers_info_list = await SellerInfo.select().where(
            (SellerInfo.city == city) &
            (SellerInfo.brand == brand) &
            (SellerInfo.working == 1) &
            (SellerInfo.availability == 1)
        ).gino.all()
    else:
        sellers_info_list = await SellerInfo.select().where(
            (SellerInfo.city == city) &
            (SellerInfo.working == 1) &
            (SellerInfo.availability == 1)
        ).gino.all()

    sellers_info_dict = {}

    if sellers_info_list:
        for i, target_seller_geodata in enumerate(sellers_info_list):
            sellers_info_dict[i] = {
                                        'city': target_seller_geodata[2],
                                        'brand': target_seller_geodata[3],
                                        'availability': target_seller_geodata[4],
                                        'working': target_seller_geodata[5],
                                        'pause': target_seller_geodata[6],
                                        'latitude': target_seller_geodata[7],
                                        'longitude': target_seller_geodata[8]
                                    }

    return sellers_info_dict
