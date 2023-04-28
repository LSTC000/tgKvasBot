from database import SecretKeys


async def get_secret_keys() -> list:
    """
    :return: Список с доступными для регистрации ключами.
    """

    secret_keys_list = await SecretKeys.query.where(SecretKeys.user_id == None).gino.all()

    secret_keys_values = [_.__dict__ for _ in secret_keys_list]

    secret_keys_list = []

    for secret_key in secret_keys_values:
        secret_keys_list.append(secret_key['__values__']['secret_key'])

    return secret_keys_list
