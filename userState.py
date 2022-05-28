from aiogram.dispatcher.filters.state import State, StatesGroup


class userState(StatesGroup):
    name = State()
    source = State()
    dest = State()
    type = State()
    flight_date = State()
    return_date = State()
class userReg(StatesGroup):
    registered = State()
    search_ticket = State()
    tickets_found = State()
