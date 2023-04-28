from loader import secret_keys_cache

from data.cache import SECRET_KEYS_CACHE_KEY

from database import update_secret_key


async def update_secret_key_from_cache(secret_key: str, user_id: int) -> None:
    """
    :param secret_key: Секретный ключ для регистрации продавца.
    :param user_id: Телеграм user id, который будет присвоен секретному ключу.
    """

    await update_secret_key(secret_key, user_id)

    if SECRET_KEYS_CACHE_KEY in secret_keys_cache:
        try:
            secret_keys_cache[SECRET_KEYS_CACHE_KEY].remove(secret_key)
        except KeyError:
            pass
