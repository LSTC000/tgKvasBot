from loader import dp, bot

from data.callbacks import DELETE_SELLER_DATA, CONFIRM_DELETE_SELLER_DATA, CANCEL_DELETE_SELLER_DATA

from data.messages import (
    MAIN_MENU_MESSAGE,
    SELLER_SETTINGS_MENU_MESSAGE,
    DELETE_SELLER_MESSAGE,
    SUCCESSFULLY_DELETE_SELLER_MESSAGE
)

from functions import reload_ikb, full_delete_seller

from keyboards import confirm_delete_seller_ikb, seller_settings_menu_ikb, main_menu_ikb

from states import MainMenuStatesGroup, SellerMenuStatesGroup, SellerSettingsStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda c: c.data == DELETE_SELLER_DATA, state=SellerMenuStatesGroup.settings_menu)
async def delete_seller(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Вызываем меню подтверждения удаления продавца.
    await reload_ikb(user_id=user_id, text=DELETE_SELLER_MESSAGE, new_ikb=confirm_delete_seller_ikb, state=state)

    await SellerSettingsStatesGroup.confirm_delete.set()


@dp.callback_query_handler(
    lambda c: c.data in [CONFIRM_DELETE_SELLER_DATA, CANCEL_DELETE_SELLER_DATA],
    state=SellerSettingsStatesGroup.confirm_delete
)
async def confirm_delete_seller(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Если продавец подтвердил удаление его аккаунта, то удаляем его и отправляем об этом сообщение.
    if callback.data == CONFIRM_DELETE_SELLER_DATA:
        await full_delete_seller(user_id)

        await bot.send_message(chat_id=user_id, text=SUCCESSFULLY_DELETE_SELLER_MESSAGE)

        # Вызываем главное меню.
        await reload_ikb(
            user_id=user_id,
            text=MAIN_MENU_MESSAGE,
            new_ikb=main_menu_ikb,
            state=state
        )

        await MainMenuStatesGroup.main_menu.set()
    else:
        # Вызываем меню настроек покупателя.
        await reload_ikb(
            user_id=user_id,
            text=SELLER_SETTINGS_MENU_MESSAGE,
            new_ikb=seller_settings_menu_ikb,
            state=state
        )

        await SellerMenuStatesGroup.settings_menu.set()
