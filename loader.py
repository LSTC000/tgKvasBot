import pytz
import logging

from data.config import (
    BOT_TOKEN,
    PARSE_MODE,
    DISABLE_WEB_PAGE_PREVIEW,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB
)

from gino import Gino

from cachetools import TTLCache

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2


__all__ = ['bot', 'dp', 'db', 'tz', 'logger']

storage = RedisStorage2(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

bot = Bot(token=BOT_TOKEN, parse_mode=PARSE_MODE, disable_web_page_preview=DISABLE_WEB_PAGE_PREVIEW)
dp = Dispatcher(bot=bot, storage=storage)

db = Gino()

# schedule_cache = TTLCache(maxsize=SCHEDULE_MAXSIZE, ttl=SCHEDULE_TTL)
# voice_cache = TTLCache(maxsize=VOICE_MAXSIZE, ttl=VOICE_TTL)

tz = pytz.timezone('Europe/Moscow')

logger = logging.getLogger(__name__)
