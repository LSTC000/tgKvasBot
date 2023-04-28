from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminMenuStatesGroup(StatesGroup):
    admin_menu = State()
    choice_secret_key = State()
