from typing import Union

from database import SellerInfo


async def get_sellers_info(city: str, brand: Union[str, None]) -> dict:
    """
    :param city: Выбранный город покупателя.
    :param brand: Выбранный бренд покупателя или None - если покупателя интересует любой бренд.
    :return: Словарь с информацией о всех подходящих продавцах.
    """

    if brand is not None:
        sellers_info_list = await SellerInfo.query.where(
            (SellerInfo.city == city) &
            (SellerInfo.brand == brand) &
            (SellerInfo.latitude.isnot(None)) &
            (SellerInfo.longitude.isnot(None)) &
            (SellerInfo.working == 1) &
            (SellerInfo.availability == 1)
        ).gino.all()
    else:
        sellers_info_list = await SellerInfo.query.where(
            (SellerInfo.city == city) &
            (SellerInfo.latitude.isnot(None)) &
            (SellerInfo.longitude.isnot(None)) &
            (SellerInfo.working == 1) &
            (SellerInfo.availability == 1)
        ).gino.all()

    sellers_info_list = [_.__dict__ for _ in sellers_info_list]

    sellers_info_dict = {}

    if sellers_info_list:
        for i, target_seller_geodata in enumerate(sellers_info_list):
            target_seller_geodata = target_seller_geodata['__values__']
            sellers_info_dict[i] = {
                                        'city': target_seller_geodata['city'],
                                        'brand': target_seller_geodata['brand'],
                                        'availability': target_seller_geodata['availability'],
                                        'working': target_seller_geodata['working'],
                                        'pause': target_seller_geodata['pause'],
                                        'latitude': target_seller_geodata['latitude'],
                                        'longitude': target_seller_geodata['longitude']
                                    }

    return sellers_info_dict
