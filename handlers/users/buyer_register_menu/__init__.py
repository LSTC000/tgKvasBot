__all__ = ['register_buyer_register_menu']


from .buyer_choice_city import buyer_choice_city, enter_buyer_choice_city
from .support_buyer_register import support_buyer_register

from aiogram import Dispatcher


def register_buyer_register_menu(dp: Dispatcher):
    dp.register_callback_query_handler(buyer_choice_city)
    dp.register_callback_query_handler(support_buyer_register)
    dp.register_callback_query_handler(enter_buyer_choice_city)
