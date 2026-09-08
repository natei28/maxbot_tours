import logging
from contextlib import suppress

#from aiogram import Bot, F, Router
from maxapi import Bot, Router, F

#from aiogram.enums import BotCommandScopeType
#from aiogram.exceptions import TelegramBadRequest
from maxapi.exceptions import MaxApiError
#from aiogram.filters import Command, CommandStart, StateFilter
from maxapi.types import MessageCreated, Command, BotCommand, BotStarted, Message,MessageCallback ,UpdateUnion
from maxapi.context import MemoryContext, StatesGroup, State


#from aiogram.fsm.context import FSMContext
#from aiogram.types import BotCommandScopeChat, CallbackQuery, Message

from app.bot.filters.filters import LocaleFilter
from app.bot.keyboards.keyboards import get_lang_settings_kb
#from app.bot.keyboards.menu_button import get_main_menu_commands
from app.bot.states.states import LangSG
from app.infrastructure.database.db import (get_user_lang, get_user_role, update_user_lang)
from psycopg import AsyncConnection

logger = logging.getLogger(__name__)

settings_router = Router()



# Этот хэндлер будет срабатывать на любые сообщения, кроме команды /start, в состоянии `LangSG.lang`
#@settings_router.message_created(F.message.body.text != "/lang" )
@settings_router.message_created(LangSG.lang, F.message.body.text != "/start" )
async def process_any_message_when_lang(
  event: UpdateUnion,
  #bot: Bot,
  user, 
  i18n: dict[str, str],
  context: MemoryContext,
  locales: list[str],
):
  user_id = user.user_id
  data = await context.get_data()
  user_lang = data.get("user_lang")

  with suppress(MaxApiError):
    msg_id = data.get("lang_settings_msg_id")
    if msg_id:
    #  await bot.edit_message_reply_markup(chat_id=user_id, message_id=msg_id)
      await event.bot.edit_message(message_id=msg_id, text="Сообщение удалено, вы в режиме выбора языка 1")

  msg = await event.message.answer(
    text=i18n.get("/lang"),
    attachments=[get_lang_settings_kb(i18n=i18n, locales=locales, checked=user_lang)],
  )

  await context.update_data(lang_settings_msg_id=msg.message.body.mid)



# Этот хэндлер будет срабатывать на команду /lang
@settings_router.message_created(Command(commands="lang"))
async def process_lang_command(
  event: UpdateUnion,
  conn: AsyncConnection,
  i18n: dict[str, str],
  user, 
  context: MemoryContext,
  locales: list[str],
):
  await context.set_state(LangSG.lang)
  user_lang = await get_user_lang(conn, user_id=user.user_id)

  msg = await event.message.answer(
    text=i18n.get("/lang"),
    attachments=[get_lang_settings_kb(i18n=i18n, locales=locales, checked=user_lang)]
    #reply_markup=get_lang_settings_kb(i18n=i18n, locales=locales, checked=user_lang),
  )
  
  #print(msg.message.body.mid)
  await context.update_data(lang_settings_msg_id=msg.message.body.mid, user_lang=user_lang)


# Этот хэндлер будет срабатывать на нажатие кнопки "Сохранить" в режиме настроек языка
@settings_router.message_callback(F.callback.payload == "save_lang_button_data")
async def process_save_click(
  event: MessageCallback, 
  #bot: Bot, 
  conn: AsyncConnection, 
  i18n: dict[str, str],
  user, 
  context: MemoryContext
):
  data = await context.get_data()
  await update_user_lang(
    conn, 
    language=data.get("user_lang"), 
    user_id=user.user_id
  )

  #await callback.message.edit_text(text=i18n.get("lang_saved"))
  
  try:
    msg_id = data.get("lang_settings_msg_id") 
    if msg_id:
      await event.bot.edit_message(
        message_id=msg_id, 
        text=i18n.get("lang_saved"),
        #text="удалено с помощью cancel", 
        #attachments=[get_lang_settings_kb(i18n=i18n, locales=locales, checked=event.callback.payload)]
      )
        #await callback.message.edit_text(text=i18n.get("lang_cancelled").format(i18n.get(user_lang)))
  except MaxApiError:
    await callback.answer()  
  
  
  await context.update_data(lang_settings_msg_id=None, user_lang=None)
  await context.set_state()  
    
'''
  user_role = await get_user_role(
    conn, 
    user_id=callback.from_user.id)
  await bot.set_my_commands(
    commands=get_main_menu_commands(i18n=i18n, role=user_role),
    scope=BotCommandScopeChat(
      type=BotCommandScopeType.CHAT,
      chat_id=callback.from_user.id
    )
  )
  '''
  
  



# Этот хэнлер будет срабатывать на нажатие кнопки "Отмена" в режиме настроек языка
@settings_router.message_callback(F.callback.payload == "cancel_lang_button_data")
async def process_cancel_click(
  event: MessageCallback, 
  conn: AsyncConnection, 
  i18n: dict[str, str],
  user, 
  context: MemoryContext
):
  print("нажата отмена")
  
  user_lang = await get_user_lang(conn, user_id=user.user_id)
  data = await context.get_data()
  
  try:
    msg_id = data.get("lang_settings_msg_id") 
    if msg_id:
      await event.bot.edit_message(
        message_id=msg_id, 
        text=i18n.get("lang_cancelled").format(i18n.get(user_lang)),
        #text="удалено с помощью cancel", 
        #attachments=[get_lang_settings_kb(i18n=i18n, locales=locales, checked=event.callback.payload)]
      )
        #await callback.message.edit_text(text=i18n.get("lang_cancelled").format(i18n.get(user_lang)))
  except MaxApiError:
    await callback.answer()
  
  await context.update_data(lang_settings_msg_id=None, user_lang=None)
  await context.set_state()
  
  

# Этот хэндлер будет срабатывать на нажатие любой радио-кнопки с локалью
# в режиме настроек языка интерфейса  LocaleFilter
#@settings_router.message_callback(F.callback.payload == "en")
@settings_router.message_callback(LocaleFilter)
async def process_lang_click(
  event: MessageCallback, 
  i18n: dict[str, str], 
  user, 
  locales: list[str], 
  context: MemoryContext,
):
  user_id = user.user_id
  data = await context.get_data()
  #user_lang = data.get("user_lang")
  try:
    #await callback.message.edit_text(
    #  text=i18n.get("/lang"),
    #  reply_markup=get_lang_settings_kb(i18n=i18n, locales=locales, checked=callback.data),
    #)
    msg_id = data.get("lang_settings_msg_id")
    if msg_id:
      await event.bot.edit_message(
          message_id=msg_id, 
          text=i18n.get("/lang"),
          attachments=[get_lang_settings_kb(i18n=i18n, locales=locales, checked=event.callback.payload)]
          )
  except MaxApiError:
    await callback.answer()
