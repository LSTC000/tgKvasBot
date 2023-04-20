__all__ = ['register_buyer_menu']


from .buyer_choice_brand import buyer_choice_brand, enter_buyer_choice_brand

from aiogram import Dispatcher


def register_buyer_menu(dp: Dispatcher):
    dp.register_callback_query_handler(buyer_choice_brand)
    dp.register_callback_query_handler(enter_buyer_choice_brand)
