from data.redis import (
    CITY_REGISTER_REDIS_KEY,
    BRAND_REGISTER_REDIS_KEY,
    IKB_PAGE_REDIS_KEY,
    NEAREST_SELLERS_REDIS_KEY
)

from aiogram.dispatcher.storage import FSMContext


async def redis_clear(state: FSMContext) -> None:
    '''
    :param state: FSMContext.
    '''

    async with state.proxy() as data:
        if CITY_REGISTER_REDIS_KEY in data:
            data.pop(CITY_REGISTER_REDIS_KEY)

        if BRAND_REGISTER_REDIS_KEY in data:
            data.pop(BRAND_REGISTER_REDIS_KEY)

        if IKB_PAGE_REDIS_KEY in data:
            data.pop(IKB_PAGE_REDIS_KEY)

        if NEAREST_SELLERS_REDIS_KEY in data:
            data.pop(NEAREST_SELLERS_REDIS_KEY)
