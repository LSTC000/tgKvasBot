import logging
from sys import maxsize

from data.config import (
    BOT_TOKEN,
    PARSE_MODE,
    DISABLE_WEB_PAGE_PREVIEW,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB,
    BUYER_MAXSIZE,
    BUYER_TTL,
    SELLER_MAXSIZE,
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
    'buyer_cache',
    'seller_cache',
    'cities_cache',
    'brands_cache'
]

storage = RedisStorage2(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

bot = Bot(token=BOT_TOKEN, parse_mode=PARSE_MODE, disable_web_page_preview=DISABLE_WEB_PAGE_PREVIEW)
dp = Dispatcher(bot=bot, storage=storage)

db = Gino()

buyer_cache = TTLCache(maxsize=BUYER_MAXSIZE, ttl=BUYER_TTL)
seller_cache = TTLCache(maxsize=SELLER_MAXSIZE, ttl=SELLER_TTL)
cities_cache = TTLCache(maxsize=CITIES_MAXSIZE, ttl=CITIES_TTL)
brands_cache = TTLCache(maxsize=BRANDS_MAXSIZE, ttl=BRANDS_TTL)

logger = logging.getLogger(__name__)
