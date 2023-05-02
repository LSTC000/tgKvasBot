from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminMenuStatesGroup(StatesGroup):
    admin_menu = State()
    create_secret_keys = State()
    show_secret_keys = State()
    delete_secret_keys = State()
