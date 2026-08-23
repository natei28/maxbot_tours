import asyncio
import logging

from app.bot.bot import main
from config.config import Config, load_config


config: Config = load_config()



logging.basicConfig(
  level=logging.getLevelName(level=config.log.level),
  format=config.log.format,
)

logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    asyncio.run(main(config))