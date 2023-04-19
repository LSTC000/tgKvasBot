from typing import List, Tuple

from database import Alerts

from sqlalchemy import select, func


async def get_alerts() -> List[Tuple[int]]:
    """
    :return: Список с пользователями, которые включили уведомления.
    """

    return await select([func.distinct(Alerts.user_id)]).gino.all()
