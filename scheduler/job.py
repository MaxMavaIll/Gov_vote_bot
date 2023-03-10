import json, os
import logging
 

from aiogram import Bot
# from aiogram.dispatcher.fsm.storage.redis import RedisStorage
from tgbot.config import load_config


path_save_file = "data/pack_for_send.json"

#from schedulers.exceptions import raise_error

async def add_user_checker(bot: Bot):
    path_file = os.path.abspath(path_save_file)
    if not os.path.exists(path_file):
        with open(path_save_file, "w") as file:
            json.dump({}, file)
    
    with open(path_save_file, "r") as file:
        data = json.load(file)
    

    logging.info(f"Data: {data}")
    config = load_config(".env")
    for ip in list(data):
        for network in data[ip]:
            for id in data[ip][network]:
                txhash = data[ip][network][id]["txhash"]
                name_wallet = data[ip][network][id]["name"]
                await bot.send_message(chat_id=config.tg_bot.chat_id, text=f"{name_wallet} {network} {id}\n"
                                                                           f"{txhash}")
        del data[ip]
    logging.info(f"Data_end: {data}")   

    with open(path_save_file, "w") as file:
        json.dump(data, file)
        
