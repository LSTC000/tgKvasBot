from typing import List, Tuple

from database import Brands

from sqlalchemy import select, func


async def get_brands() -> List[Tuple[str]]:
    """
    :return: Список с доступных брендов.
    """

    return await select([func.distinct(Brands.brand)]).gino.all()
