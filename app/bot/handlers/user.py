import logging
from contextlib import suppress

from maxapi import Bot, Router, F
#from aiogram.enums import BotCommandScopeType
from maxapi.exceptions import MaxApiError
#from aiogram.filters import KICKED, ChatMemberUpdatedFilter, Command, CommandStart
from maxapi.types import MessageCreated, Command, BotCommand, BotStarted, Message, UpdateUnion
#from maxapi.types import UpdateUnion, User, MessageCallback, Message

from maxapi.context import MemoryContext, StatesGroup, State

#from aiogram.fsm.context import FSMContext
#from aiogram.types import BotCommandScopeChat, ChatMemberUpdated, Message
from app.bot.enums.roles import UserRole
#from app.bot.keyboards.menu_button import get_main_menu_commands
from app.bot.states.states import LangSG
from app.infrastructure.database.db import (
  add_user,
  change_user_alive_status,
  get_user,
  get_user_lang,
)
from psycopg.connection_async import AsyncConnection

logger = logging.getLogger(__name__)

# Инициализируем роутер уровня модуля
user_router = Router()


# Этот хэндлер срабатывает на команду /start
@user_router.message_created(Command("start"))
async def process_start_command(
  event: UpdateUnion, 
  conn: AsyncConnection, 
  #bot: Bot,
  user, 
  i18n: dict[str, str], 
  context: MemoryContext, 
  admin_ids: list[int],
  translations: dict
):
  user_row = await get_user(conn, user_id=user.user_id)
  if user_row is None:
    if user.user_id in admin_ids:
      user_role = UserRole.ADMIN
    else:
      user_role = UserRole.USER
    await add_user(
      conn,
      user_id=user.user_id,
      username=user.username,
      language="ru",
      role=user_role
    )
  else:
    user_role = UserRole(user_row[4])
    await change_user_alive_status(
      conn, 
      is_alive=True, 
      user_id=user.user_id, 
    )

  if await context.get_state() == LangSG.lang:
    data = await context.get_data()
    with suppress(MaxApiError):
      msg_id = data.get("lang_settings_msg_id")
      if msg_id:
        #await bot.edit_message_reply_markup(chat_id=message.from_user.id, message_id=msg_id)
        await event.bot.edit_message(message_id=msg_id, text="Сообщение удалено")
      user_lang = await get_user_lang(conn, user_id=user.user_id)
      i18n = translations.get(user_lang)

  #await bot.set_my_commands(
  #  commands=get_main_menu_commands(i18n=i18n, role=user_role),
  #  scope=BotCommandScopeChat(
  #    type=BotCommandScopeType.CHAT,
  #    chat_id=message.from_user.id
  #  )
  #)

  await event.message.answer(text=i18n.get("/start"))
  await context.clear()