from database import Alerts


async def get_alert(user_id: int) -> bool:
    """
    :param user_id: Телеграм user id.
    :return: True, если пользователь включил уведомления, иначе - False.
    """

    return True if await Alerts.query.where(Alerts.user_id == user_id).gino.all() else False
