from aiogram.dispatcher.filters.state import StatesGroup, State


class BuyerMenuStatesGroup(StatesGroup):
    choice_brand = State()
