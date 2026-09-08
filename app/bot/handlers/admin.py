import logging


from maxapi import Bot, Router, F
from maxapi.types import MessageCreated, Command, BotCommand, BotStarted, Message, MessageCallback, UpdateUnion

#from aiogram import Router
#from aiogram.filters import Command, CommandObject
#from aiogram.types import Message

from app.bot.enums.roles import UserRole
from app.bot.filters.filters import UserRoleFilter
from app.infrastructure.database.db import (
    change_user_banned_status_by_id,
    change_user_banned_status_by_username,
    get_statistics,
    get_user_banned_status_by_id,
    get_user_banned_status_by_username,
)
from psycopg import AsyncConnection

logger = logging.getLogger(__name__)

admin_router = Router()

admin_router.filter(UserRoleFilter(UserRole.USER))

# Этот хэндлер будет срабатывать на команду /help для пользователя с ролью `UserRole.ADMIN`
@admin_router.message_created(Command(commands="help"))
async def process_admin_help_command(event: MessageCreated, i18n: dict):
  await event.message.answer(text=i18n.get('/help_admin'))
  
  
# Этот хэндлер будет срабатывать на команду /statistics для пользователя с ролью `UserRole.ADMIN`
@admin_router.message_created(Command(commands='statistics'))
async def process_admin_statistics_command(event: MessageCreated, conn: AsyncConnection, i18n: dict[str, str]):
  statistics = await get_statistics(conn)
  await event.message.answer(
    text=i18n.get("statistics").format(
        "\n".join(
            f"{i}. <b>{stat[0]}</b>: {stat[1]}"
            for i, stat in enumerate(statistics, 1)
        )
    )
  )  