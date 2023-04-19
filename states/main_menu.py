from aiogram.dispatcher.filters.state import StatesGroup, State


class MainMenuStatesGroup(StatesGroup):
    main_menu = State()
    buyer_menu = State()
    seller_menu = State()
