__all__ = ['register_main_menu']


from .buyer_settings_menu import buyer_settings_menu

from aiogram import Dispatcher


def register_main_menu(dp: Dispatcher):
    dp.register_callback_query_handler(buyer_settings_menu)
