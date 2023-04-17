from loader import logger

from asyncpg import UniqueViolationError

from database import SellerCoordinates


async def add_seller_coordinates(
    seller_id: int,
    city: str,
    latitude: str = None,
    longitude: str = None
) -> None:
    '''
    :param seller_id: Телеграм user id.
    :param city: Название города.
    :param latitude: Широта. По умолчанию: None.
    :param longitude: Долгота. По умолчанию: None.
    :return: None.
    '''

    try:
        seller_coordinates = SellerCoordinates(seller_id=seller_id, city=city, latitude=latitude, longitude=longitude)
        await seller_coordinates.create()
    except UniqueViolationError:
        logger.info('Error to add seller coordinates! Seller coordinates already exists in the database.')
