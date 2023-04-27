from database import Alerts

from sqlalchemy import select, func


async def get_alerts() -> list:
    """
    :return: Список с пользователями, которые включили уведомления.
    """

    return await select([Alerts.distinct(Alerts.user_id)]).gino.all()
