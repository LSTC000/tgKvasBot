from aiogram.dispatcher.filters.state import StatesGroup, State


class BuyerRegisterMenuStatesGroup(StatesGroup):
    register_menu = State()
    choice_city = State()
    choice_brand = State()
