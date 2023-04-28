__all__ = ['register_admin_menu']


from .create_secret_key import generate_secret_key
from .choice_secret_key import show_available_secret_keys, choice_secret_key

from aiogram import Dispatcher


def register_admin_menu(dp: Dispatcher):
    dp.register_callback_query_handler(generate_secret_key)
    dp.register_callback_query_handler(show_available_secret_keys)
    dp.register_callback_query_handler(choice_secret_key)
