from database import Alerts

from sqlalchemy import select, func
from sqlalchemy.exc import ArgumentError


async def get_alerts() -> list:
    """
    :return: Список с пользователями, которые включили уведомления.
    """

    try:
        return await select([func.distinct(Alerts.user_id)]).gino.all()
    except ArgumentError:
        return []
