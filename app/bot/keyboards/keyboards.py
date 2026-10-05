#from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from maxapi.types import MessageCreated, MessageCallback
from maxapi.types.attachments.attachment import ButtonsPayload
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder
from maxapi.types.attachments.buttons import (
    ClipboardButton,
    LinkButton,
    CallbackButton,
)

from maxapi.context import MemoryContext, StatesGroup, State


def get_lang_settings_kb(i18n: dict, locales: list[str], checked: str) -> ButtonsPayload:
    buttons = []
    for locale in sorted(locales):
        if locale == "default":
            continue
        if locale == checked:
            buttons.append(
                [
                    CallbackButton(
                        text=f"🔘 {i18n.get(locale)}", payload=locale
                    )
                ]
            )
        else:
            buttons.append(
                [
                    CallbackButton(
                        text=f"⚪️ {i18n.get(locale)}", payload=locale
                    )
                ]
            )
    buttons.append(
        [
            CallbackButton(
                text=i18n.get("cancel_lang_button_text"), 
                payload="cancel_lang_button_data"
            ),
            CallbackButton(
                text=i18n.get("save_lang_button_text"), 
                payload="save_lang_button_data"
            ),
        ]
    )
    return ButtonsPayload(buttons=buttons).pack()
    

'''
Фунция вызова клавиатуры Menu
'''    

def get_menu_kb():
    menu_builder = InlineKeyboardBuilder()
    menu_builder.row(
        CallbackButton(text="Заполнить анкету!", payload="start_ankets"))
    menu_builder.row(
        CallbackButton(text="Подобрать отель с ИИ", payload="start_ankets"))
    menu_builder.row(
        CallbackButton(text="О нас!", payload="about_as"),
        CallbackButton(text="Полезное", payload="profits"))
    return menu_builder.as_markup()

   
   
# Вызов клавиатуры в виде чекбоксов / чеклиста   

def check_list(ITEM, selected):
    
    #if type(event).__name__ == 'MessageCallback':
    #    payload = event.callback.payload
    #    if payload in item_checked[user_id]:
    #        index_payload = item_checked[user_id].index(payload)
    #        item_checked[user_id].pop(index_payload)
    #    else:
    #        item_checked[user_id].append(payload)
    
    #print(stars_checked)
    buttons =[]
    for i in ITEM:
        if i in selected :
            buttons.append([CallbackButton(text=f"🔘 {i}", payload=i)])
        else:
            buttons.append([CallbackButton(text=f"⚪️ {i}", payload=i)])
            
    kb = ButtonsPayload(buttons=buttons).pack()
    #checked = item_checked[user_id]
    
    return kb

def multi_select_3(items, selected, kb_type='block', act_btns=True):
     builder = InlineKeyboardBuilder()
     
     if kb_type == 'block':
         for i in items:
             if i in selected:
                 builder.row(CallbackButton(text=f"🔘 {i}", payload=i))
             else:
                 builder.row(CallbackButton(text=f"⚪️ {i}", payload=i))    
     elif kb_type == 'inline':
         buttons =[]
         for i in items:
             if i in selected :
                 buttons.append(CallbackButton(text=f"🔘 {i}", payload=i))
             else:
                 buttons.append(CallbackButton(text=f"⚪️ {i}", payload=i))
         builder.row(*buttons)   
         
     builder.row(
         CallbackButton(text="Отмена", payload="cancel_select"),
         CallbackButton(text="Сохранить", payload="save_select"))
         
     kb = builder.as_markup()
     return kb 
     
     
def multi_select_1(items, selected, colls=2, act_btns=True):
     builder = InlineKeyboardBuilder()
     buttons =[]
     
     for i in range(0, len(items), colls):
         buttons =[]
         for n in items[i:i+colls]:
             if n in selected:
                 buttons.append(CallbackButton(text=f"🔘 {n}", payload=n))
             else:
                 buttons.append(CallbackButton(text=f"⚪️ {n}", payload=n))
         builder.row(*buttons)   
         
     builder.row(
         CallbackButton(text="Отмена", payload="cancel_select"),
         CallbackButton(text="Сохранить", payload="save_select"))
         
     kb = builder.as_markup()
     return kb
     
     
def multi_select_2(items, selected, size=2, act_btns=True):
    
    result = []
    current_chunk = []
    current_step = 0

    for item in items:
        if current_step < size:
            current_chunk.append(item)
            current_step +=1
        
        else:
            if current_chunk:
                result.append(current_chunk)
            current_step=1
            current_chunk=[item]
         
    if current_chunk:
        result.append(current_chunk) 
     
    
    builder = InlineKeyboardBuilder()
    buttons =[]
     
    for i in result:
        buttons =[]
        for n in i:
            if n in selected:
                buttons.append(CallbackButton(text=f"🔘 {n}", payload=n))
            else:
                buttons.append(CallbackButton(text=f"⚪️ {n}", payload=n))
        builder.row(*buttons)   
         
    builder.row(
        CallbackButton(text="Отмена", payload="cancel_select"),
        CallbackButton(text="Сохранить", payload="save_select"))
         
    kb = builder.as_markup()
    return kb 




    
async def select_fun(
    event,
    context: MemoryContext,
    selected_name
):
    
    data = await context.get_data()
    selected = data.get(selected_name)
    
    if not selected:
        selected = []
        await context.update_data(**{selected_name:selected})
    
    if not isinstance(event, MessageCallback):
        return selected
    
    payload = event.callback.payload
    
    if payload is None:
        return selected
        
    if payload in selected:
        selected = [x for x in selected if x != payload]
    else:
        selected = selected + [payload]
    
    await context.update_data(**{selected_name:selected})
    
    return selected
    
   
    
def multi_select(items, selected=[], size=5, act_btns=True):
    '''
    Это функция вызова клавиатуры в виде обычной клавиатуры,
    мульти-селекта.
    
    Передаваемые параметры:
        'items'     - обязательный параметр, основной список элементов, 
                      передаются в text и payload
                      
        'selected'  - по умолчанию = [], список выбранных элементов, 
                      передается извне, берется из контекста, если не передавать
                      список, будет работатьккак обыч.клавиатура

        'size'      - по умолчанию 5, суммарная длина строки в символах,
                      подстраивает количество кнопок по длине
    '''
    if size <= 0:
        raise ValueError("size должен быть > 0")

    
    result = []
    current_chunk = []
    current_len = 0

    for item in items:
        item_len = len(item)
    
        if current_len == 0 and item_len > size:
            result.append([item])
            continue
    
        if current_len + item_len <= size:
            current_chunk.append(item)
            current_len += item_len
        
        else:
            if current_chunk:
                result.append(current_chunk)  
            current_chunk = [item]
            current_len = item_len    
    if current_chunk:
        result.append(current_chunk)    
     
    
    builder = InlineKeyboardBuilder()
    buttons =[]
     
    for i in result:
        buttons =[]
        for n in i:
            if n in selected:
                buttons.append(CallbackButton(text=f"🔘 {n}", payload=n))
            else:
                buttons.append(CallbackButton(text=f"⚪ {n}", payload=n))
        builder.row(*buttons)   
         
    builder.row(
        CallbackButton(text="Отмена", payload="cancel_select"),
        CallbackButton(text="Сохранить", payload="save_select"))
         
    kb = builder.as_markup()
    return kb          
     