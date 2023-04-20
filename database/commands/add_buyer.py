from typing import Union

from loader import logger

from asyncpg import UniqueViolationError

from database import Buyer


async def add_buyer(buyer_id: int, city: str, brand: Union[str, None]) -> None:
    '''
    :param buyer_id: Телеграм user id.
    :param city: Название города.
    :param brand: Название бренда. Если бренд не выбран - None.
    :return: None.
    '''

    try:
        buyer = Buyer(buyer_id=buyer_id, city=city, brand=brand)
        await buyer.create()
    except UniqueViolationError:
        logger.info('Error to add buyer! Buyer already exists in the database.')
