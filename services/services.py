import asyncio
import random
import logging
from maxapi import Bot
from maxapi.types import BotCommand


# Создаем список с командами и их описанием для кнопки menu
async def set_main_menu(bot: Bot):
  await bot.set_my_commands(
    BotCommand(name="start", description="Запустика ты бота"),
    BotCommand(name="help", description="Показать справку"),
    BotCommand(name="menu", description="Главное меню"),
    BotCommand(name="settings", description="Настройки"),
    BotCommand(name="support", description="Техподдержка"),
  )
  
async def msg_delay(event):
    chat_id = event.chat.chat_id
    await event.bot.send_action(chat_id=chat_id)
    await asyncio.sleep(2)