from aiogram.dispatcher.filters.state import StatesGroup, State


class BuyerSettingsStatesGroup(StatesGroup):
    settings_menu = State()
    change_city = State()
