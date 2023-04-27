from loader import dp, bot

from data.messages import (
    SELLER_MENU_MESSAGE,
    SELLER_UPDATE_GEODATA_MESSAGE,
    SUCCESSFULLY_SELLER_UPDATE_GEODATA_MESSAGE
)

from keyboards import seller_menu_ikb, seller_update_geodata_menu_rkb

from functions import (
    reload_ikb,
    reload_rkb,
    get_seller_menu_ikb_params,
    update_seller_latitude_from_cache,
    update_seller_longitude_from_cache
)

from states import MainMenuStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.message_handler(content_types=types.ContentTypes.LOCATION, state=MainMenuStatesGroup.seller_menu)
async def seller_update_geodata(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    # Достаём широту и долготу.
    latitude = message.location.latitude
    longitude = message.location.longitude

    # Добавляем в БД координаты продавца.
    await update_seller_latitude_from_cache(user_id, latitude)
    await update_seller_longitude_from_cache(user_id, longitude)

    await bot.send_message(chat_id=user_id, text=SUCCESSFULLY_SELLER_UPDATE_GEODATA_MESSAGE)

    # Вызываем меню продавца.
    await reload_ikb(
        user_id=user_id,
        text=SELLER_MENU_MESSAGE,
        new_ikb=seller_menu_ikb,
        state=state,
        ikb_params=await get_seller_menu_ikb_params(user_id)
    )
    await reload_rkb(
        user_id=user_id,
        text=SELLER_UPDATE_GEODATA_MESSAGE,
        new_rkb=seller_update_geodata_menu_rkb,
        state=state
    )
