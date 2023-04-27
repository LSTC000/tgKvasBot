from database import Brands

from sqlalchemy import select, func


async def get_brands() -> list:
    """
    :return: Список с доступных брендов.
    """

    return await select([func.distinct(Brands.brand)]).gino.all()
