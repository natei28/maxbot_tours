import asyncio
import logging


from config_data.config import Config, load_config
from services.services import set_main_menu

from maxapi.context import MemoryContext, StatesGroup, State


from maxapi import Bot, Dispatcher, Router, F
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder

from maxapi.enums import ParseMode

from maxapi.types import MessageCreated, Command, BotCommand, BotStarted
from maxapi.types.attachments.attachment import ButtonsPayload
from maxapi.types.attachments.buttons import (
    ClipboardButton,
    LinkButton,
    CallbackButton,
)


logging.basicConfig(level=logging.INFO)

#bot = Bot('f9LHodD0cOIuPDhcjlAUsdHGLlC5pfwDWcU9sizPaPkftqF8zJdKSyo9mG2MzrFRRnn8c5MScyx5iyRL4Rx-')
#dp = Dispatcher()

class FSM_Form(StatesGroup):
  name = State()
  age = State()



builder = InlineKeyboardBuilder()
builder.row(
    LinkButton(text="Сайт", url="https://example.com"),
    CallbackButton(text="○ Нажми", payload="data"))
builder.row(ClipboardButton(text="Скопировать код", payload="ABC-123"))
builder.row(CallbackButton(text="Ещё кнопка", payload="more"))


buttons = [
    [LinkButton(text="Сайт", url="https://example.com")],
    [ClipboardButton(text="Скопировать код", payload="ABC-123")],
    [CallbackButton(text="Callback", payload="data")]
]
payload = ButtonsPayload(buttons=buttons).pack()
  
#async def set_main_menu(bot: Bot):
# Создаем список с командами и их описанием для кнопки menu
#  await bot.set_my_commands(
#            BotCommand(name="start", description="Запустика бота"),
#            BotCommand(name="help", description="Показать справку"),
#            BotCommand(name="menu", description="Главное меню"),
#            BotCommand(name="settings", description="Настройки"),
#            BotCommand(name="support", description="Техподдержка"),
#  )
        

async def main():
  # Загружаем конфиг в переменную config
  config: Config = load_config()
  # Инициализируем бот и диспетчер
  bot = Bot(
    token=config.max_bot.token,
    parse_mode=ParseMode.HTML)
  dp = Dispatcher()


  @dp.bot_started()
  async def bot_started(event: BotStarted):
    await event.bot.send_message(
      chat_id=event.chat_id,
      text='Привет! Отправь мне /start')

  @dp.message_created(Command('start'))
  async def start_handler(event: MessageCreated, context: MemoryContext):
    await context.set_state(FSM_Form.name)
    await event.message.answer('Как Вас зовут?')

  @dp.message_created(FSM_Form.name)
  async def name_handler(event: MessageCreated, context: MemoryContext):
    await context.update_data(name=event.message.body.text)
    await context.set_state(FSM_Form.age)
    await event.message.answer('Сколько Вам лет?')

  @dp.message_created(FSM_Form.age)
  async def age_handler(event: MessageCreated, context: MemoryContext):
    await context.update_data(age=event.message.body.text)
    data = await context.get_data()
    await event.message.answer(
      f'Приятно познакомится,{data["name"]}'
      f"Вам {data['age']} лет.")
      
    await bot.send_message(
      chat_id=376728607,
      text="good")
    await context.set_state(None)
 
    
  @dp.message_created(Command('help'))
  async def echo(event: MessageCreated):
    await event.message.answer(
      text="Клавиатура:",
      attachments=[payload])
  
  
  
  # Пропускаем накопившиеся апдейты и запускаем polling
  await set_main_menu(bot)
  
#  dp.include_routers(user_handlers.router)
  
  await bot.delete_webhook()
  await dp.start_polling(bot)
  
asyncio.run(main())


