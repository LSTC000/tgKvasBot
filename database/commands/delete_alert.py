from database import Alerts


async def delete_alert(user_id: int):
    """
    :param user_id: Телеграм user id, у которого мы отключим уведомления.
    """

    return await Alerts.delete.where(Alerts.user_id == user_id).gino.scalar()
