from database import SellerGeodata


async def get_seller_geodata(seller_id: int) -> dict:
    """
    :param seller_id: Телеграм user id.
    :return: Список с данными продавца.
    """

    seller_geodata_list = await SellerGeodata.query.where(SellerGeodata.seller_id == seller_id).gino.all()
    seller_geodata_values = [seller_geodata.__dict__ for seller_geodata in seller_geodata_list]
    return seller_geodata_values[0]['__values__']
