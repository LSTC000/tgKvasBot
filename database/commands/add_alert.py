from loader import logger

from asyncpg import UniqueViolationError

from database import Alerts


async def add_alert(user_id: int) -> None:
    '''
    :param user_id: Телеграм user id.
    :return: None.
    '''

    try:
        alert = Alerts(user_id=user_id)
        await alert.create()
    except UniqueViolationError:
        logger.info('Error to alert! Alerts already exists in the database.')
