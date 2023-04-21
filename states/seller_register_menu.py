from aiogram.dispatcher.filters.state import StatesGroup, State


class SellerRegisterMenuStatesGroup(StatesGroup):
    register_menu = State()
    choice_city = State()
    choice_brand = State()
    register_code = State()
