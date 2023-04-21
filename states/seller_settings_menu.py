from aiogram.dispatcher.filters.state import StatesGroup, State


class SellerSettingsStatesGroup(StatesGroup):
    change_city = State()
    change_brand = State()
    confirm_delete = State()
