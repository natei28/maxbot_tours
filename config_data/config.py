from dataclasses import dataclass
from environs import Env 

@dataclass
class MaxBot:
  token: str
  
@dataclass
class Config:
  max_bot: MaxBot
  
def load_config(path: str | None = None) -> Config:
  env = Env()
  env.read_env(path)
  return Config(max_bot=MaxBot(token=env('BOT_TOKEN')))