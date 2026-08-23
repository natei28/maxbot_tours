import asyncio
import logging

import uvicorn
from fastapi import FastAPI

from maxapi import Bot, Dispatcher, Router, F
from maxapi.types import MessageCreated

import uvicorn
from fastapi import FastAPI
from maxapi.webhook.fastapi import FastAPIMaxWebhook





from maxapi.filters.filter import BaseFilter
from maxapi.types import MessageCallback, Message





#from app.bot.handlers.admin import admin_router
#from app.bot.handlers.others import others_router
#from app.bot.handlers.settings import settings_router
#from app.bot.handlers.user import user_router
from app.bot.i18n.translator import get_translations
from app.bot.middlewares.global_data import GlobalDataMiddleware
#from app.bot.middlewares.database import DataBaseMiddleware
#from app.bot.middlewares.i18n import TranslatorMiddleware
#from app.bot.middlewares.lang_settings import LangSettingsMiddleware
#from app.bot.middlewares.shadow_ban import ShadowBanMiddleware
#from app.bot.middlewares.statistics import ActivityCounterMiddleware


from app.infrastructure.database.connection import get_pg_pool
from config.config import Config, load_config


from redis.asyncio import Redis
from maxapi.context import MemoryContext, StatesGroup, State, RedisContext



from maxapi.enums import ParseMode


from maxapi.types import MessageCreated, Command, BotCommand, BotStarted

from maxapi.utils.inline_keyboard import InlineKeyboardBuilder
from maxapi.types.attachments.attachment import ButtonsPayload
from maxapi.types.attachments.buttons import (
    ClipboardButton,
    LinkButton,
    CallbackButton,
 )

from services.services import set_main_menu




logging.basicConfig(level=logging.INFO)


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


logger = logging.getLogger(__name__)


################# Рабочий фильтр #########################
##########################################################
#from maxapi.filters.filter import BaseFilter
#from maxapi.types import MessageCallback, Message

#class MyFilter(BaseFilter):                          
#  async def __call__(self, event: MessageCallback):  
#    print(f'Gришло Hello {event.callback.payload}')  
#     return str(event.callback.payload) == "data"

#class MyFilter(BaseFilter):                          
#  async def __call__(self, event: Message):  
#    print(f'Gришло Hello {event.from_user}')  
#    return int(event.from_user.user_id) == 81169128      

#@dp.message_callback(MyFilter())
#    async def handle_specific_callback(event: MessageCallback):
#        await event.message.answer("Это кнопка с payload='data'!")

#@dp.message_callback(MyFilter())
#    async def handle_specific_callback(event: MessageCallback):
#        await event.message.answer("Это кнопка с payload='data'!")
    
#    @dp.message_created(MyFilter())
#    async def handle_specific_callback(event: Message):
#        await event.message.answer(f"Фильтр на  проверку user_id = {event.from_user.user_id}!")

#########################################################



async def main(config: Config) -> None:
    logger.info("Starting bot...")
    
    #bot = Bot(token='f9LHodD0cOIuPDhcjlAUsdHGLlC5pfwDWcU9sizPaPkftqF8zJdKSyo9mG2MzrFRRnn8c5MScyx5iyRL4Rx-')
    #dp = Dispatcher()
    # Инициализируем бот и диспетчер
        
    redis_client = Redis(
        host=config.redis.host,
        port=config.redis.port,
        db=config.redis.db,
        password=config.redis.password,
        username=config.redis.username,
    )
    
    bot = Bot(
        token=config.max_bot.token,
        parse_mode=ParseMode.HTML)
    
    dp = Dispatcher(
        storage=RedisContext,
        redis_client=redis_client,
        key_prefix="my_bot"
    )
    
    
    # Создаём пул соединений с Postgres
    db_pool: psycopg_pool.AsyncConnectionPool = await get_pg_pool(
        db_name=config.db.name,
        host=config.db.host,
        port=config.db.port,
        user=config.db.user,
        password=config.db.password,
    )
    
    # Получаем словарь с переводами
    translations = get_translations()
    # формируем список локалей из ключей словаря с переводами
    locales = list(translations.keys())
    
    
    
    
    
    @dp.message_created()
    async def handle_message(event: MessageCreated):
        await event.message.answer('Бот работает через вебхуки!')
        await event.message.answer(text="Клавиатура",attachments=[payload],)
        
    
    
    
    # Подключаем роутеры в нужном порядке
#    logger.info("Including routers...")
#    dp.include_routers(settings_router, admin_router, user_router, others_router)

    # Подключаем миддлвари в нужном порядке
    logger.info("Including middlewares...")
#    dp.register_inner_middleware(GlobalDataMiddleware(db_pool, transltions, locales))
    dp.register_inner_middleware(GlobalDataMiddleware(db_pool, translations, locales))
#    dp.update.middleware(DataBaseMiddleware())
#    dp.update.middleware(ShadowBanMiddleware())
#    dp.update.middleware(ActivityCounterMiddleware())
#    dp.update.middleware(LangSettingsMiddleware())
#    dp.update.middleware(TranslatorMiddleware())
    
    
    
    
    
    
    
    
    
    
    
    
    
    webhook_url = 'https://lili-ufa.ru/webhook'  # <-- укажите свой
    webhook_secret = 'ayaz112017_465935387'      # <-- укажите свой (5–256 символов)

    # Передаём secret в конструктор — он сохраняется в webhook.secret.
    # Фреймворк будет автоматически проверять заголовок X-Max-Bot-Api-Secret
    # в каждом входящем POST-запросе и возвращать 403 при несоответствии.
    webhook = FastAPIMaxWebhook(dp=dp, bot=bot, secret=webhook_secret)

    # Создаём FastAPI-приложение с lifespan-инициализацией диспетчера
    app = FastAPI(lifespan=webhook.lifespan)

    # Собственные маршруты — например, healthcheck
    @app.get('/health')
    async def health():
        return {'status': 'ok'}

    # Подключаем MAX webhook-обработчик к нашему приложению
    webhook.setup(app, path='/webhook')

    # Подписываемся на webhook — передаём тот же secret,
    # чтобы платформа MAX добавляла X-Max-Bot-Api-Secret в каждый запрос.
    await bot.subscribe_webhook(url=webhook_url, secret=webhook_secret)

    # Запускаем сервер uvicorn
    config = uvicorn.Config(app=app, host='0.0.0.0', port=8080)
    server = uvicorn.Server(config)
    await server.serve()


