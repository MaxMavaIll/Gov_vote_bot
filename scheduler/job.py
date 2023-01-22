import json
import logging
from aiogram import Bot
# from aiogram.dispatcher.fsm.storage.redis import RedisStorage
from tgbot.config import load_config


path_save_file = "data/pack_for_send.json"

#from schedulers.exceptions import raise_error

async def add_user_checker(bot: Bot):
    with open(path_save_file, "r") as file:
        data = json.load(file)
    
    logging.info(f"Data: {data}")
    config = load_config(".env")
    for ip in list(data):
        for id in data[ip]:
            txhash = data[ip][id]["txhash"]
            await bot.send_message(chat_id=config.tg_bot.chat_id, text=f"Cyber {id} {txhash}")
        del data[ip]
    logging.info(f"Data_end: {data}")   

    with open(path_save_file, "w") as file:
        data = json.dump(data, file)
        
