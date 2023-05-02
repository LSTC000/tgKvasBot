from loader import secret_keys_cache

from data.cache import SECRET_KEYS_CACHE_KEY

from database import delete_secret_key


async def delete_available_secret_key_from_cache(secret_key: str) -> None:
    '''
    :param secret_key: Секретный ключ, который мы будем удалять.
    '''

    # Удаляем cекретный ключ продавца из БД.
    await delete_secret_key(secret_key)

    # Если ключ в кэше, то удаляем его оттуда.
    if SECRET_KEYS_CACHE_KEY in secret_keys_cache:
        if secret_key in secret_keys_cache[SECRET_KEYS_CACHE_KEY]:
            secret_keys_cache[SECRET_KEYS_CACHE_KEY].remove(secret_key)
