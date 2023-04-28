from typing import Union

from loader import logger

from asyncpg import UniqueViolationError

from database import SecretKeys


async def add_secret_key(secret_key: str, user_id: Union[int, None] = None) -> None:
    '''
    :param secret_key: Секретный ключ для регистрации продавца.
    :param user_id: Телеграм user id, который будет присвоен секретному ключу. По умолчанию - None.
    :return: None.
    '''

    try:
        secret_key = SecretKeys(user_id=user_id, secret_key=secret_key)
        await secret_key.create()
    except UniqueViolationError:
        logger.info('Error to add secret key! Secret key already exists in the database.')
