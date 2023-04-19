from loader import logger

from asyncpg import UniqueViolationError

from database import Cities


async def add_city(city: str) -> None:
    '''
    :param city: Название города.
    :return: None.
    '''

    try:
        city = Cities(city=city)
        await city.create()
    except UniqueViolationError:
        logger.info('Error to add city! Cities already exists in the database.')
