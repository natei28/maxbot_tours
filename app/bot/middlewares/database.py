import logging
from typing import Any, Awaitable, Callable

from maxapi.filters.middleware import BaseMiddleware
from psycopg_pool import AsyncConnectionPool

from maxapi.types import UpdateUnion


logger = logging.getLogger(__name__)

class DataBaseMiddleware(BaseMiddleware):
  async def __call__(
    self,
    handler: Callable[[UpdateUnion, dict[str, Any]], Awaitable[Any]],
    event: UpdateUnion,
    data: dict[str, Any],
  ) -> Any:
    db_pool: AsyncConnectionPool = data.get("db_pool")

    if db_pool is None:
      logger.error("Database pool is not provided in middleware data.")
      raise RuntimeError("Missing db_pool in middleware context.")

    async with db_pool.connection() as connection:
      try:
        async with connection.transaction():
          data["conn"] = connection
          result = await handler(event, data)
      except Exception as e:
        logger.exception("Transaction rolled back due to error: %s", e)
        raise
    
    var_3 = data["conn"]
    print(f"Прошел, мидл датабэйс, data['con']= {var_3}"    )    
    # Здесь может быть какой-то код, который выполнится в случае успешного завершения транзакции        

    return result