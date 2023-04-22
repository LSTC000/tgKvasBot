from loader import dp

from data.messages import SELLER_UPDATE_GEODATA_RKB_MESSAGE

from database import (
    update_seller_latitude,
    update_seller_longitude,
    update_seller_address,
    update_seller_address_url
)

from functions import create_seller_address_url

from states import MainMenuStatesGroup

from aiogram import types


@dp.message_handler(lambda m: m.text == SELLER_UPDATE_GEODATA_RKB_MESSAGE, state=MainMenuStatesGroup.seller_menu)
async def seller_change_geodata(message: types.Message) -> None:
    user_id = message.from_user.id

    # Достаём широту и долготу.
    latitude = message.location.latitude
    longitude = message.location.longitude

    # Достаём адрес и URL адрес покупателя.
    seller_address_url = create_seller_address_url(user_id=user_id, longitude=longitude, latitude=latitude)

    # Если мы получили geodata покупателя, то добавляем его в БД, иначе отпраялем сообщение об ошибке.
    if seller_address_url is not None:
        address, address_url = seller_address_url[0], seller_address_url[1]

        await update_seller_latitude(user_id, latitude)
        await update_seller_longitude(user_id, longitude)
        await update_seller_address(user_id, address)
        await update_seller_address_url(user_id, address_url)
