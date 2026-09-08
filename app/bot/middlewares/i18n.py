import logging
from typing import Any, Awaitable, Callable

from maxapi.filters.middleware import BaseMiddleware
from maxapi.types import UpdateUnion, User, MessageCallback, Message
from maxapi.context import MemoryContext, StatesGroup, State
from psycopg import AsyncConnection
from app.infrastructure.database.db import get_user_lang

logger = logging.getLogger(__name__)


class TranslatorMiddleware(BaseMiddleware):
  async def __call__(
    self,
    handler: Callable[[UpdateUnion, dict[str, Any]], Awaitable[Any]],
    event: UpdateUnion,
    data: dict[str, Any],
  ) -> Any:
  
    logger.info("[MIDDLEWARE START] %s", self.__class__.__name__)
    
    user: User = data.get("user")

    if user is None:
      return await handler(event, data)


    logger.info("[MIDDLEWARE END_1] %s", self.__class__.__name__)
    
    context: MemoryContext = data.get('context')
    #print(context)
    translations: dict = data.get("translations") 
    if context is None:
      data["i18n"] = translations[translations["default"]] 
      return await handler(event, data)  
    user_context_data = await context.get_data()
    
    logger.info("[MIDDLEWARE END_2] %s", self.__class__.__name__)
    
    #print("юзерлэнг из контекста:")
    #print(user_context_data.get('user_lang'))
    
    if (user_lang := user_context_data.get('user_lang')) is None:
      conn: AsyncConnection = data.get("conn")
      if conn is None:
        logger.error("Database connection not found in middleware data.")
        raise RuntimeError("Missing database connection for detecting the user's language.")

      user_lang: str | None = await get_user_lang(conn, user_id=user.user_id)
      if user_lang is None:
        user_lang = user.language_code

    #print("user_lang:")
    #print(user_lang)
    
    #translations: dict = data.get("translations")
    i18n: dict = translations.get(user_lang) 

    if i18n is None:
      data["i18n"] = translations[translations["default"]]
    else:
      data["i18n"] = i18n
    #print(" Перевод i18n:")  
    #print(data["i18n"])
    
    
    logger.info("[MIDDLEWARE END] %s", self.__class__.__name__)
    return await handler(event, data)