from typing import Union

from database import SellerGeodata, SellerInfo


async def get_sellers_data(city: str, brand: Union[str, None]) -> dict:
    """
    :param city: Выбранный город покупателя.
    :param brand: Выбранный бренд покупателя или None - если покупателя интересует любой бренд.
    :return: Словарь с данными всех продавцов.
    """

    query = SellerGeodata.join(SellerInfo, SellerGeodata.seller_id == SellerInfo.seller_id)
    if brand is not None:
        sellers_data_list = await query.select().where(
            (SellerGeodata.city == city) &
            (SellerGeodata.brand == brand) &
            (SellerInfo.working == 1) &
            (SellerInfo.availability == 1)
        ).gino.all()
    else:
        sellers_data_list = await query.select().where(
            (SellerGeodata.city == city) &
            (SellerInfo.working == 1) &
            (SellerInfo.availability == 1)
        ).gino.all()

    sellers_data_dict = {}

    if sellers_data_list:
        for i, target_seller_geodata in enumerate(sellers_data_list):
            sellers_data_dict[i] = {
                                        'city': target_seller_geodata[2],
                                        'brand': target_seller_geodata[3],
                                        'latitude': target_seller_geodata[4],
                                        'longitude': target_seller_geodata[5],
                                        'availability': target_seller_geodata[9],
                                        'working': target_seller_geodata[10],
                                        'pause': target_seller_geodata[11],
                                    }

    return sellers_data_dict
