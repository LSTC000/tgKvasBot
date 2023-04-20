__all__ = ['register_buyer_register_menu']


from .buyer_choice_city import buyer_choice_city, enter_buyer_choice_city
from .buyer_choice_brand import buyer_choice_brand, enter_buyer_choice_brand
from .buyer_confirm_register import buyer_confirm_register
from .support_buyer_register import support_buyer_register

from aiogram import Dispatcher


def register_buyer_register_menu(dp: Dispatcher):
    dp.register_callback_query_handler(buyer_choice_city)
    dp.register_callback_query_handler(enter_buyer_choice_city)
    dp.register_callback_query_handler(buyer_choice_brand)
    dp.register_callback_query_handler(enter_buyer_choice_brand)
    dp.register_callback_query_handler(buyer_confirm_register)
    dp.register_callback_query_handler(support_buyer_register)
