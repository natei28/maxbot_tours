
###     Эта мидлварь для того чтоб передать в data (workflowdata) обьекты locales, translations,   ###
###     db_pool, для использования в следующих мидлварях.                                          ###

import logging
from typing import Any, Awaitable, Callable
from maxapi.filters.middleware import BaseMiddleware
from psycopg_pool import AsyncConnectionPool

logger = logging.getLogger(__name__)

class GlobalDataMiddleware(BaseMiddleware):
    def __init__(self, db_pool, translations, locales):
        self.db_pool = db_pool
        self.translations = translations
        self.locales = locales
        
    async def __call__(self, handler, event, data):
        data["db_pool"] = self.db_pool
        data["translations"] = self.translations
        data["locales"] = self.locales
        var_1 = data.get("locales")
        var_2 = data.get("db_pool")
        print(var_1)
        print(var_2)
        return await handler(event, data)

