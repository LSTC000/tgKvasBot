__all__ = ['register_seller_register_menu']


from .seller_choice_city import seller_choice_city, enter_seller_choice_city
from .seller_choice_brand import seller_choice_brand, enter_seller_choice_brand
from .seller_confirm_register import seller_confirm_register, enter_seller_register_code
from .support_seller_register import support_seller_register

from aiogram import Dispatcher


def register_seller_register_menu(dp: Dispatcher):
    dp.register_callback_query_handler(seller_choice_city)
    dp.register_callback_query_handler(enter_seller_choice_city)
    dp.register_callback_query_handler(seller_choice_brand)
    dp.register_callback_query_handler(enter_seller_choice_brand)
    dp.register_callback_query_handler(seller_confirm_register)
    dp.register_message_handler(enter_seller_register_code)
    dp.register_callback_query_handler(support_seller_register)
