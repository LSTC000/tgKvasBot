from database import SellerGeodata


async def delete_seller_geodata(seller_id: int):
    """
    :param seller_id: Телеграм user id.
    """

    return await SellerGeodata.delete.where(SellerGeodata.seller_id == seller_id).gino.scalar()
