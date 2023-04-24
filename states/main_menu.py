from aiogram.dispatcher.filters.state import StatesGroup, State


class MainMenuStatesGroup(StatesGroup):
    main_menu = State()
    find_nearest_seller = State()
    seller_menu = State()
    settings_menu = State()
