__all__ = ['register_buyer_settings_menu']


from .buyer_change_city import buyer_change_city, enter_buyer_change_city
from .buyer_change_alert import buyer_change_alert

from aiogram import Dispatcher


def register_buyer_settings_menu(dp: Dispatcher):
    dp.register_callback_query_handler(buyer_change_city)
    dp.register_callback_query_handler(enter_buyer_change_city)
    dp.register_callback_query_handler(buyer_change_alert)
