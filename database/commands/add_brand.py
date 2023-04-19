from loader import logger

from asyncpg import UniqueViolationError

from database import Brands


async def add_brand(
    brand: str
) -> None:
    '''
    :param brand: Название бренда.
    :return: None.
    '''

    try:
        brand = Brands(brand=brand)
        await brand.create()
    except UniqueViolationError:
        logger.info('Error to add brand! Brands already exists in the database.')
