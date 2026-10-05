import logging
from typing import Any, Awaitable, Callable

from maxapi.filters.middleware import BaseMiddleware
from maxapi.types import UpdateUnion, User, MessageCallback, Message
from maxapi.context import MemoryContext, StatesGroup, State

#from aiogram.fsm.context import FSMContext

logger = logging.getLogger(__name__)


class LangSettingsMiddleware(BaseMiddleware):
  async def __call__(
    self,
    handler: Callable[[UpdateUnion, dict[str, Any]], Awaitable[Any]],
    event: UpdateUnion,
    data: dict[str, Any],
  ) -> Any:
    user: User = data.get("user")
    if user is None:
      return await handler(event, data)
      
    if not isinstance(event, MessageCallback):
      #print(f"Евент не MessageCallback, а {type(event).__name__}")
      return await handler(event, data)            

    if event.callback.payload is None:
      return await handler(event,  data)

    locales: list[str] = data.get('locales')

    context: MemoryContext = data.get('context')
        
    #print(f"контекст: {context}")
    #print(f"Евент MessageCallback {event.callback}")
    #print(f"Евент: {event.message.sender.locale}")
    '''
    
    '''
    if context is None:
      #print(f"Апдейт {event.from_user}")  
      return await handler(event, data)
      logger.info("Context is None")
       
    
    user_context_data: dict = await context.get_data()

    if event.callback.payload == "cancel_lang_button_data":
      user_context_data.update(user_lang=None)
      await context.set_data(user_context_data)

    elif event.callback.payload in locales and event.callback.payload != user_context_data.get('user_lang'):
      user_context_data.update(user_lang=event.callback.payload)
      await context.set_data(user_context_data)

    return await handler(event, data)