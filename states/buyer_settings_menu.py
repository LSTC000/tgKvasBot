from aiogram.dispatcher.filters.state import StatesGroup, State


class BuyerSettingsStatesGroup(StatesGroup):
    change_city = State()
    change_brand = State()
