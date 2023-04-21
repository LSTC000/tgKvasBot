__all__ = ['register_users_cancels_menu']


from .cancel_to_main_menu import cancel_to_main_menu
from .cancel_to_seller_menu import cancel_to_seller_menu

from aiogram import Dispatcher


def register_users_cancels_menu(dp: Dispatcher):
    dp.register_callback_query_handler(cancel_to_main_menu)
    dp.register_callback_query_handler(cancel_to_seller_menu)
