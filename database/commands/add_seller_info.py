from loader import logger

from asyncpg import UniqueViolationError

from database import SellerInfo


async def add_seller_info(
    seller_id: int,
    city: str,
    brand: str,
    availability: int = 0,
    working: int = 0,
    pause: int = 1,
    latitude: str = None,
    longitude: str = None
) -> None:
    '''
    :param seller_id: Телеграм user id.
    :param city: Название города.
    :param brand: Название бренда кваса.
    :param availability: Наличие кваса: 0 - нет, 1 - есть. По умолчанию: 0.
    :param working: Рабочие день: 0 - закончен, 1 - не закончен. По умолчанию: 0.
    :param pause: Перерыв: 0 - продавец работает, 1 - продавец ушёл на перерыв. По умолчанию: 1.
    :param latitude: Широта. По умолчанию: None.
    :param longitude: Долгота. По умолчанию: None.
    :return: None.
    '''

    try:
        seller_info = SellerInfo(
            seller_id=seller_id,
            city=city,
            brand=brand,
            availability=availability,
            working=working,
            pause=pause,
            latitude=latitude,
            longitude=longitude
        )
        await seller_info.create()
    except UniqueViolationError:
        logger.info('Error to add seller info! Seller info already exists in the database.')
