from loader import dp, bot

from data.messages import (
    SELLER_MENU_MESSAGE,
    SELLER_UPDATE_GEODATA_MESSAGE,
    SUCCESSFULLY_SELLER_UPDATE_GEODATA_MESSAGE,
    ERROR_SELLER_UPDATE_GEODATA_MESSAGE
)

from database import (
    update_seller_latitude,
    update_seller_longitude,
    update_seller_address,
    update_seller_address_url
)

from keyboards import seller_menu_ikb, seller_update_geodata_menu_rkb

from functions import create_seller_address_url, reload_ikb, reload_rkb, get_seller_menu_ikb_params

from states import MainMenuStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.message_handler(content_types=types.ContentTypes.LOCATION, state=MainMenuStatesGroup.seller_menu)
async def seller_update_geodata(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    # Достаём широту и долготу.
    latitude = str(message.location.latitude)
    longitude = str(message.location.longitude)

    # Достаём адрес и URL адрес покупателя.
    seller_address_url = await create_seller_address_url(user_id=user_id, latitude=latitude, longitude=longitude)

    # Если мы получили геоданные покупателя, то добавляем его в БД, иначе отправляем сообщение об ошибке.
    if seller_address_url is not None:
        address, address_url = seller_address_url[0], seller_address_url[1]

        await update_seller_latitude(user_id, latitude)
        await update_seller_longitude(user_id, longitude)
        await update_seller_address(user_id, address)
        await update_seller_address_url(user_id, address_url)

        await bot.send_message(chat_id=user_id, text=SUCCESSFULLY_SELLER_UPDATE_GEODATA_MESSAGE)
    else:
        await bot.send_message(chat_id=user_id, text=ERROR_SELLER_UPDATE_GEODATA_MESSAGE)

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
