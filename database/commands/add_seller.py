from loader import logger

from asyncpg import UniqueViolationError

from database import Seller


async def add_seller(seller_id: int) -> None:
    '''
    :param seller_id: Телеграм user id.
    :return: None.
    '''

    try:
        seller = Seller(seller_id=seller_id)
        await seller.create()
    except UniqueViolationError:
        logger.info('Error to add seller! Seller already exists in the database.')
