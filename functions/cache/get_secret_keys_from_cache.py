from loader import secret_keys_cache

from data.cache import SECRET_KEYS_CACHE_KEY

from database import get_secret_keys


async def get_secret_keys_from_cache() -> list:
    """
    :return: Список доступных ключей.
    """

    if SECRET_KEYS_CACHE_KEY in secret_keys_cache:
        secret_keys = secret_keys_cache[SECRET_KEYS_CACHE_KEY]
    else:
        secret_keys = await get_secret_keys()
        secret_keys_cache[SECRET_KEYS_CACHE_KEY] = secret_keys

    return secret_keys
