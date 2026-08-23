#from aiogram.filters import BaseFilter
#from aiogram.types import CallbackQuery, Message

from maxapi.filters.filter import BaseFilter
from maxapi.types import MessageCallback, Message

#class MyFilter(BaseFilter):                          
#  async def __call__(self, event: MessageCallback):  
#    print(f'Gришло Hello {event.callback.payload}')  
#     return str(event.callback.payload) == "data"


from psycopg import AsyncConnection

from app.bot.enums.roles import UserRole
from app.infrastructure.database.db import get_user_role



class LocaleFilter(BaseFilter):
  async def __call__(self, event: MessageCallback, locales: list):
    if not isinstance(event, MessageCallback):
      raise ValueError(
        f"LocaleFilter: expected `MessageCallback`, got `{type(event).__name__}`"
      )
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

  async def __call__(self, event: Message | MessageCallback, conn: AsyncConnection) -> bool:
    user = event.from_user
      if not user:
        return False

    role = await get_user_role(conn, user_id=user.id)
      if role is None:
        return False
        
    return role in self.roles