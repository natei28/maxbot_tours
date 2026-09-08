import logging
from typing import Any, Awaitable, Callable

from maxapi.filters.middleware import BaseMiddleware
from maxapi.types import UpdateUnion, User
from app.infrastructure.database.db import add_user_activity, get_user, get_user_role
from psycopg import AsyncConnection

logger = logging.getLogger(__name__)


class ActivityCounterMiddleware(BaseMiddleware):
  async def __call__(
    self,
    handler: Callable[[UpdateUnion, dict[str, Any]], Awaitable[Any]],
    event: UpdateUnion,
    data: dict[str, Any],
  ) -> Any:
  
    logger.info("[MIDDLEWARE START] %s", self.__class__.__name__) 
    

    user: User = data.get("user")
    #print(f"Юзер: {user}")
    #print(f"Юзер id: {user.user_id}")
    
    if user is None:
      return await handler(event, data)

    
    conn: AsyncConnection = data.get("conn")
    if conn is None:
      logger.error("No database connection found in middleware data.")
      raise RuntimeError("Missing database connection for activity logging.")
    
    user_in_db = await get_user(conn, user_id=user.user_id)
    role_in_db = await get_user_role(conn, user_id=user.user_id)
    data["role_in_db"] = role_in_db
    
    #context.set_data(user_in_db=user_in_db)
    
    #print(f"юзер из бд: {user_in_db}")
    #print(data.get('locales'))
    
    if user_in_db is None:
        return await handler(event, data)
    
    await add_user_activity(conn, user_id=user.user_id)
    
    
    print(event)    
    logger.info("[MIDDLEWARE END] %s", self.__class__.__name__)
    
    return await handler(event, data)