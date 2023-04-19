from loader import logger

from asyncpg import UniqueViolationError

from database import Buyer


async def add_buyer(buyer_id: int, city: str) -> None:
    '''
    :param buyer_id: Телеграм user id.
    :param city: Название города.
    :return: None.
    '''

    try:
        buyer = Buyer(buyer_id=buyer_id, city=city)
        await buyer.create()
    except UniqueViolationError:
        logger.info('Error to add buyer! Buyer already exists in the database.')
