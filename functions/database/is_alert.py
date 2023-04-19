from database import get_alerts


async def is_alert(user_id: int) -> bool:
    """
    :param user_id: Телеграм user id.
    :return: True - если у пользователя включены уведомления, иначе - False.
    """

    alerts = await get_alerts()
    for user in alerts:
        if user_id == user[0]:
            return True

    return False
