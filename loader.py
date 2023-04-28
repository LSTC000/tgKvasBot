import logging

from data.config import (
    BOT_TOKEN,
    PARSE_MODE,
    DISABLE_WEB_PAGE_PREVIEW,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB,
    SECRET_KEYS_MAXSIZE,
    SECRET_KEYS_TTL,
    BUYER_INFO_MAXSIZE,
    BUYER_TTL,
    SELLER_INFO_MAXSIZE,
    SELLER_TTL,
    CITIES_MAXSIZE,
    CITIES_TTL,
    BRANDS_MAXSIZE,
    BRANDS_TTL
)

from gino import Gino

from cachetools import TTLCache

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2


__all__ = [
    'bot',
    'dp',
    'db',
    'logger',
    'secret_keys_cache',
    'buyer_info_cache',
    'seller_info_cache',
    'cities_cache',
    'brands_cache'
]

storage = RedisStorage2(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

bot = Bot(token=BOT_TOKEN, parse_mode=PARSE_MODE, disable_web_page_preview=DISABLE_WEB_PAGE_PREVIEW)
dp = Dispatcher(bot=bot, storage=storage)

db = Gino()

secret_keys_cache = TTLCache(maxsize=SECRET_KEYS_MAXSIZE, ttl=SECRET_KEYS_TTL)
buyer_info_cache = TTLCache(maxsize=BUYER_INFO_MAXSIZE, ttl=BUYER_TTL)
seller_info_cache = TTLCache(maxsize=SELLER_INFO_MAXSIZE, ttl=SELLER_TTL)
cities_cache = TTLCache(maxsize=CITIES_MAXSIZE, ttl=CITIES_TTL)
brands_cache = TTLCache(maxsize=BRANDS_MAXSIZE, ttl=BRANDS_TTL)

logger = logging.getLogger(__name__)
