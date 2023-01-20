
from dataclasses import dataclass
from typing import List
from environs import Env

@dataclass
class Tg_bot:
    token: str
    admin_ids: List[int]
    user_redis: bool

@dataclass
class DBConfig:
    host: str
    password: str
    user: str
    database: str

@dataclass
class Miscellaneus:
    other_params: str = None

@dataclass
class Config:
    tg_bot: Tg_bot
    db: DBConfig
    misc: Miscellaneus

def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=Tg_bot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            user_redis=env.bool("USE_REDIS")
        ), 
        db=DBConfig(
            host=env.str("DB_HOST"),
            password=env.str("DB_PASS"),
            user=env.str("DB_USER"),
            database=env.str("DB_NAME")
        ),
        misc=Miscellaneus()
    )