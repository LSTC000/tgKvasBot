__all__ = ['register_seller_menu']


from .seller_change_availability import seller_change_availability
from .seller_change_working import seller_change_working
from .seller_change_pause import seller_change_pause
from .seller_settings_menu import seller_settings_menu

from aiogram import Dispatcher


def register_seller_menu(dp: Dispatcher):
    dp.register_callback_query_handler(seller_change_availability)
    dp.register_callback_query_handler(seller_change_working)
    dp.register_callback_query_handler(seller_change_pause)
    dp.register_callback_query_handler(seller_settings_menu)
