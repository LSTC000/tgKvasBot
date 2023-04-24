from loader import logger

from asyncpg import UniqueViolationError

from database import SellerGeodata


async def add_seller_geodata(
    seller_id: int,
    city: str,
    brand: str,
    latitude: str = None,
    longitude: str = None
) -> None:
    '''
    :param seller_id: Телеграм user id.
    :param city: Название города.
    :param brand: Название бренда кваса.
    :param latitude: Широта. По умолчанию: None.
    :param longitude: Долгота. По умолчанию: None.
    :return: None.
    '''

    try:
        seller_address = SellerGeodata(
            seller_id=seller_id,
            city=city,
            brand=brand,
            latitude=latitude,
            longitude=longitude
        )
        await seller_address.create()
    except UniqueViolationError:
        logger.info('Error to add seller geodata! Seller geodata already exists in the database.')
