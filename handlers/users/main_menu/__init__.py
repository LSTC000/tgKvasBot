__all__ = ['register_main_menu']


from .find_nearest_seller import find_nearest_seller, find_next_nearest_seller
from .buyer_settings_menu import buyer_settings_menu
from .seller_menu import seller_menu

from aiogram import Dispatcher


def register_main_menu(dp: Dispatcher):
    dp.register_message_handler(find_nearest_seller)
    dp.register_callback_query_handler(find_next_nearest_seller)
    dp.register_callback_query_handler(buyer_settings_menu)
    dp.register_callback_query_handler(seller_menu)
