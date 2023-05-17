__all__ = ['register_admin_menu']


from .count_secret_keys import count_secret_keys
from .create_secret_keys import enter_count_create_secret_keys, create_secret_keys
from .show_secret_keys import enter_count_show_secret_keys, show_secret_keys
from .delete_secret_keys import enter_count_delete_secret_keys, delete_secret_keys
from .alert_for_users import enter_alert_for_users, alert_for_users

from aiogram import Dispatcher


def register_admin_menu(dp: Dispatcher):
    dp.register_callback_query_handler(count_secret_keys)
    dp.register_callback_query_handler(enter_count_create_secret_keys)
    dp.register_message_handler(create_secret_keys)
    dp.register_callback_query_handler(enter_count_show_secret_keys)
    dp.register_message_handler(show_secret_keys)
    dp.register_callback_query_handler(enter_count_delete_secret_keys)
    dp.register_message_handler(delete_secret_keys)
    dp.register_callback_query_handler(enter_alert_for_users)
    dp.register_message_handler(alert_for_users)
