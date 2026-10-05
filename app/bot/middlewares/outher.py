import logging
from typing import Any, Awaitable, Callable

from maxapi.filters.middleware import BaseMiddleware
from maxapi.types import UpdateUnion, User
from app.infrastructure.database.db import add_user_activity, get_user, get_user_role
from psycopg import AsyncConnection


class DataInjectionMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        print("!!!")
        print(data)
        user: User = data.get("user")
        data["user"] = user
        return await handler(event, data)
