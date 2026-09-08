from maxapi.context import MemoryContext, StatesGroup, State, RedisContext


class LangSG(StatesGroup):
    lang = State()