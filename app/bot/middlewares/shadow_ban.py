import logging
from typing import Any, Awaitable, Callable

from maxapi.filters.middleware import BaseMiddleware
from maxapi.types import UpdateUnion, User

from app.infrastructure.database.db import get_user_banned_status_by_id
from psycopg import AsyncConnection




logger = logging.getLogger(__name__)


class ShadowBanMiddleware(BaseMiddleware):
  async def __call__(
    self,
    handler: Callable[[UpdateUnion, dict[str, Any]], Awaitable[Any]],
    event: UpdateUnion,
    data: dict[str, Any],
  ) -> Any:
  
    logger.info("[MIDDLEWARE START] %s", self.__class__.__name__)
    
    user: User = data.get("user")
    #user: User = event.from_user
    #print("вошли в мидлварь shadowban")
    #print(user)
    #print(event)
    
    
    if user is None:
      return await handler(event, data)

    conn: AsyncConnection = data.get("conn")
    if conn is None:
      logger.error("Database connection not found in middleware data.")
      raise RuntimeError("Missing database connection for shadow ban check.")

    user_banned_status = await get_user_banned_status_by_id(conn, user_id=user.user_id)

    if user_banned_status:
      logger.warning("Shadow-banned user tried to interact: %d", user.user_id)
      if event.callback:
        await event.message.answer()
      return 
    
    logger.info("[MIDDLEWARE END] %s", self.__class__.__name__)
    
    return await handler(event, data)