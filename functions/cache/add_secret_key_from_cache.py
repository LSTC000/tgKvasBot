from loader import secret_keys_cache

from data.cache import SECRET_KEYS_CACHE_KEY

from database import add_secret_key, get_secret_keys

from utils import create_secret_key


async def add_secret_key_from_cache() -> None:
    secret_key = create_secret_key()

    # Добавляем новый секретный ключ в БД.
    await add_secret_key(secret_key)

    if SECRET_KEYS_CACHE_KEY in secret_keys_cache:
        secret_keys_cache[SECRET_KEYS_CACHE_KEY].append(secret_key)
    else:
        secret_keys_cache[SECRET_KEYS_CACHE_KEY] = await get_secret_keys()
