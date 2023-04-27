from database import Cities

from sqlalchemy import select, func


async def get_cities() -> list:
    """
    :return: Список с доступными городами.
    """

    return await select([func.distinct(Cities.city)]).gino.all()
