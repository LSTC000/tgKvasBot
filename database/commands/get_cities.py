from typing import List, Tuple

from database import Cities

from sqlalchemy import select, func


async def get_cities() -> List[Tuple[str]]:
    """
    :return: Список с доступными городами.
    """

    return await select([func.distinct(Cities.city)]).gino.all()
