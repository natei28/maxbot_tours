import asyncio
import random
import logging
from contextlib import suppress

from maxapi import Bot, Router, F
from maxapi.exceptions import MaxApiError
from maxapi.types import MessageCreated, Command, BotCommand, BotStarted, Message, UpdateUnion, MessageCallback

from maxapi.context import MemoryContext, StatesGroup, State

from app.bot.enums.roles import UserRole
from app.bot.keyboards.keyboards import get_menu_kb, check_list, multi_select, multi_select_1, multi_select_2, multi_select_3, select_fun
from app.bot.states.states import AnketsSG
from app.infrastructure.database.db import (
  add_user,
  change_user_alive_status,
  get_user,
  get_user_lang,
)
from services.services import msg_delay
from psycopg.connection_async import AsyncConnection

logger = logging.getLogger(__name__)

# Инициализируем роутер уровня модуля
user_anket_router = Router()




### Шаг 1. Сюда попадаем когда юзер нажмет "заполнить анкету"

#Хэндлер будет срабатывать на нажатие кнопки "Заполнить анкету"
@user_anket_router.message_callback(F.callback.payload == "start_ankets")
async def process_start_ankets(
    event: MessageCallback,
    i18n: dict[str, str],
    context: MemoryContext
):
  
  await msg_delay(event)
  await event.message.answer(text=random.choice(i18n["good_task"]))
  
  await msg_delay(event)
  await event.message.answer(text=i18n["get_name"])
  await context.set_state(AnketsSG.name)

  
### Шаг 2. Попадаем после ввода арлтщователем "Имени"

# Хэндлер будет срабатывать на ввод в состоянии Ankets.name
@user_anket_router.message_created(AnketsSG.name) 
async def process_get_name(
    event: MessageCreated,
    i18n: dict[str, str],
    context: MemoryContext):
    
    text = (event.message.body.text or "").strip()
	
    await msg_delay(event)
    
    if not text:
        await event.message.answer(text=i18n["get_name_nottext"])
        return
    if len(text) < 2:
        await event.message.answer(text=i18n["get_name_minlen"])
        return
    if any(ch.isdigit() for ch in text):
        await event.message.answer(text=i18n["get_name_nostr"])
        return    
    
    await context.update_data(name=text)
    await event.message.answer(text=i18n["get_age"])
    await context.set_state(AnketsSG.age)


### Шаг 3. Попадаем при вводе юзером "возраста".
### Выдаем клавиатуру, также предлагаем ввод

# Хэндлер будет срабатывать на ввод в состоянии Ankets.fio
@user_anket_router.message_created(AnketsSG.age)
async def process_get_age(
    event: MessageCreated,
    i18n: dict[str, str],
    context: MemoryContext
):
    text = (event.message.body.text or "").strip()
    
    if not text or not text.isdigit():
        await event.message.answer(text=i18n["get_age_nottext"])
        return 
    
    await context.update_data(age=text)
    
    await msg_delay(event)
    await event.message.answer(text=random.choice(i18n["good_task"]))
    await msg_delay(event)
    
    dep_city_selected = await select_fun(
        event, context, 
        selected_name = 'dep_city_selected')
	
    kb = multi_select_3(
        i18n["main_city"],
        dep_city_selected)
    
    msg = await event.message.answer(
            text = i18n["get_dep_city"],
            attachments = [kb])             
    
    await context.update_data(dep_city_msg_id=msg.message.body.mid)
    await context.set_state(AnketsSG.dep_city)
        
		
### Шаг 4. Попадаем при нажатии юзером города, либо ручном вводе города

# Этот хэндлер обработывет нажатие кнопок в состоянии AnketsSG.dep_city
@user_anket_router.message_callback(AnketsSG.dep_city)
async def get_dep_city_process(
    event: MessageCallback,
    i18n: dict[str, str],
    context: MemoryContext
):
    
    #data = await context.get_data()
    '''
    dep_city_selected = data.get('dep_city_selected')
    
    if not dep_city_selected:
        dep_city_selected = []
        await context.update_data(dep_city_selected = dep_city_selected)
    
    payload = event.callback.payload
    if payload in dep_city_selected:
        index_payload = dep_city_selected.index(payload)
        dep_city_selected.pop(index_payload)
    else:
        dep_city_selected.append(payload)
    
    await context.update_data(dep_city_selected = dep_city_selected)
    
    '''
    
    dep_city_selected = await select_fun(event, context, selected_name = 'dep_city_selected')
    data = await context.get_data()
    
    kd = multi_select_3(
        i18n["main_city"], 
        dep_city_selected)
    
    try:
        msg_id = data.get("dep_city_msg_id")
        if msg_id:
            await event.bot.edit_message(
                message_id=msg_id, 
                text=i18n.get("выбирете один или несколько, либо отправте текстом"),
                attachments=[kd]
            )
    except MaxApiError:
        await callback.answer()
		
		
# Этот хэндлер будет обрабатывать ввод текста в состоянии AnkeysSG.dep_city
@user_anket_router.message_created(AnketsSG.dep_city)
async def get_dep_city_2(
	event: MessageCreated,
	context: MemoryContext,
	i18n: dict[str, str]
):
	text = (event.message.body.text or "").strip()
	await event.message.answer(
		text = f"Вы ввели{text}"
	)
	await event.message.answer(
		text = "Куда желаете отправится?"
	)


'''
STARS = ['Москва', 'уфа', 'Санкт-Петербур', 'Сочи', 'Крым']  
#STARS = ['⭐⭐⭐', '⭐⭐⭐⭐','⭐⭐⭐⭐⭐']
  
  
# Хэндлер будет срабатывать на ввод в состоянии Ankets.fio
@user_router.message_created(AnketsSG.fio) 
async def process_get_fio(
    event: MessageCreated,
    i18n: dict[str, str],
    user,
    context: MemoryContext
):
    await context.update_data(client_fio=event.message.body.text)
    
    data = await context.get_data()
    stars_selected = data.get('stars_selected')
    if not stars_selected:
        stars_selected = []
        await context.update_data(stars_selected = stars_selected)
    
    
    keyboard = multi_select_3(
        STARS,
        stars_selected,
    )
    
    msg = await event.message.answer(
        text=f"вы ввели:{event.message.body.text}",
        attachments=[keyboard]
    )
    
    await context.update_data(hotel_star_msg_id=msg.message.body.mid)
    await context.set_state(AnketsSG.hotel_star)
    #await context.update_data
    data = await context.get_data()
    print(data)
    print(await context.get_state())
    




    
# Хэндлер будет срабатывать на выбор звезд отеля
@user_router.message_callback(AnketsSG.hotel_star, F.callback.payload.in_(STARS))  
async def process_get_hotel_star(
    event: MessageCallback,
    i18n: dict[str, str],
    context: MemoryContext
):
    
    data = await context.get_data()
    stars_selected = data.get('stars_selected')
    
    if not stars_selected:
        stars_selected = []
        await context.update_data(stars_selected = stars_selected)
    
    payload = event.callback.payload
    if payload in stars_selected:
        index_payload = stars_selected.index(payload)
        stars_selected.pop(index_payload)
    else:
        stars_selected.append(payload)
    
    await context.update_data(stars_selected=stars_selected)
    
    keyboard = multi_select_3(
        STARS, 
        stars_selected,
    )
    
    data = await context.get_data()
    try:
        msg_id = data.get("hotel_star_msg_id")
        if msg_id:
            await event.bot.edit_message(
                message_id=msg_id, 
                text=i18n.get("выбирете один или несколько"),
                attachments=[keyboard]
            )
    except MaxApiError:
        await callback.answer()
        
#
# Хэндлер будет срабатывать при нажатии кнопки отмена при выборе отеля
#
#@user_router.message_callback(AnketsSG.hotel_star, F.callback.payload in STARS)  
@user_router.message_callback(AnketsSG.hotel_star, F.callback.payload == "cancel_select")
async def process_cancel_star(
    event: MessageCallback,
    i18n: dict[str, str],
    context: MemoryContext
):
    print("\\\\\\\\\\\\\\\\\\\\\\")
    
    data = await context.get_data()
    
    stars_selected = []
    await context.update_data(stars_selected = stars_selected)
    
    keyboard = multi_select_3(
        STARS, 
        stars_selected
    )
    data = await context.get_data()
    try:
        msg_id = data.get("hotel_star_msg_id")
        if msg_id:
            await event.bot.edit_message(
                message_id=msg_id, 
                text=i18n.get("выбирете один или несколько"),
                attachments=[keyboard]
            )
    except MaxApiError:
        await callback.answer()
        
        '''