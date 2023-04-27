__all__ = ['register_seller_settings_menu']


from .seller_change_city import seller_change_city, enter_seller_change_city
from .seller_change_brand import seller_change_brand, enter_seller_change_brand
from .delete_seller import delete_seller_info_from_cache, confirm_delete_seller

from aiogram import Dispatcher


def register_seller_settings_menu(dp: Dispatcher):
    dp.register_callback_query_handler(seller_change_city)
    dp.register_callback_query_handler(enter_seller_change_city)
    dp.register_callback_query_handler(seller_change_brand)
    dp.register_callback_query_handler(enter_seller_change_brand)

