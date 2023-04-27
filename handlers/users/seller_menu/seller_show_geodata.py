from loader import dp, bot

from data.callbacks import SHOW_GEODATA_DATA

from data.messages import SELLER_MENU_MESSAGE, SELLER_UPDATE_GEODATA_MESSAGE, NONE_SELLER_GEODATA_MESSAGE

from functions import reload_ikb, reload_rkb, get_seller_menu_ikb_params, get_seller_geodata

from keyboards import seller_menu_ikb, seller_update_geodata_menu_rkb

from states import MainMenuStatesGroup

from utils import create_seller_geodata_report

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda c: c.data == SHOW_GEODATA_DATA, state=MainMenuStatesGroup.seller_menu)
async def seller_show_geodata(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    seller_geodata_dict = await get_seller_geodata(user_id)

    # Отправляем пользователю информацию о геоданных, если они есть.
    if seller_geodata_dict is not None:
        await bot.send_message(chat_id=user_id, text=create_seller_geodata_report(seller_geodata_dict))
        await bot.send_location(
            chat_id=user_id,
            latitude=seller_geodata_dict['latitude'],
            longitude=seller_geodata_dict['longitude']
        )
    else:
        await bot.send_message(chat_id=user_id, text=NONE_SELLER_GEODATA_MESSAGE)

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
