from typing import Union

from loader import logger

from asyncpg import UniqueViolationError

from database import BuyerInfo


async def add_buyer_info(buyer_id: int, city: str, brand: Union[str, None]) -> None:
    '''
    :param buyer_id: Телеграм user id.
    :param city: Название города.
    :param brand: Название бренда. Если бренд не выбран - None.
    :return: None.
    '''

    try:
        buyer_info = BuyerInfo(buyer_id=buyer_id, city=city, brand=brand)
        await buyer_info.create()
    except UniqueViolationError:
        logger.info('Error to add buyer info! Buyer info already exists in the database.')
