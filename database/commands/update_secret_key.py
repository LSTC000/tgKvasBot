from database import SecretKeys


async def update_secret_key(secret_key: str, user_id: int) -> None:
    '''
    :param secret_key: Секретный ключ для регистрации продавца.
    :param user_id: Телеграм user id, который будет присвоен секретному ключу.
    :return: None.
    '''

    await SecretKeys.update.values(user_id=user_id).where(SecretKeys.secret_key == secret_key).gino.scalar()
