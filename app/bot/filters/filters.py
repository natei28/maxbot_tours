#from aiogram.filters import BaseFilter
#from aiogram.types import CallbackQuery, Message

from maxapi.filters.filter import BaseFilter
from maxapi.types import MessageCallback, Message
from typing import Any, Awaitable, Callable
#class MyFilter(BaseFilter):                          
#  async def __call__(self, event: MessageCallback):  
#    print(f'Gришло Hello {event.callback.payload}')  
#     return str(event.callback.payload) == "data"


from psycopg import AsyncConnection

from app.bot.enums.roles import UserRole
from app.infrastructure.database.db import get_user_role



class LocaleFilter(BaseFilter):
  async def __call__(
      self, 
      event: MessageCallback, 
      data: dict[str, Any]):
      
    if not isinstance(event, MessageCallback):
      raise ValueError(
        f"LocaleFilter: expected `MessageCallback`, got `{type(event).__name__}`"
      )
    
    locales: list[str] = data.get('locales')
    if locales is None:
      # можно либо вернуть False, либо кинуть ошибку — зависит от твоей логики
      return False
    #print(localesl) 
     
    return event.callback.payload in locales


class UserRoleFilter(BaseFilter):
  def __init__(self, *roles: str | UserRole):
    if not roles:
      raise ValueError("At least one role must be provided to UserRoleFilter.")

    self.roles = frozenset(
      UserRole(role) if isinstance(role, str) else role
        for role in roles
          if isinstance(role, (str, UserRole))
    )

    if not self.roles:
      raise ValueError("No valid roles provided to `UserRoleFilter`.")

  async def __call__(
    self, 
    message: Message | MessageCallback,
    role_in_db, 
    user
  ) -> bool:
    print('!!!!!!!')
    
    #role = data.get("role")
    #print(role)
    #user = data.get("user")
    #print(user)
    print(role_in_db)
    print(user)
    if not user:
      return False

    #role = await get_user_role(conn, user_id=user.user_id)
    if role_in_db is None:
      return False
        
    return role_in_db in self.roles