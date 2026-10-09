from maxapi.context import MemoryContext, StatesGroup, State, RedisContext


class LangSG(StatesGroup):
    lang = State()

class AnketsSG(StatesGroup):
    start = State()
    name = State()
    age = State()
    dep_city = State()
    destn = State()
    abults = State()

    travel_dates = State()
    abult_count = State()
    children_count = State()
    budget = State()
    hotel_stars = State()
    
    hotel_star = State()
    age = State()
    male = State()
    mobile = State()
