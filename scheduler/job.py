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
                if data[ip][network][id]["txhash"] != '':
                    txhash = data[ip][network][id]["txhash"]
                    name_wallet = data[ip][network][id]["name"]
                    await bot.send_message(chat_id=config.tg_bot.chat_id, text=f"{name_wallet} {network} {id}\n"
                                                                           f"{txhash}")
                else:
                    error = data[ip][network][id]["error"]
                    name_wallet = data[ip][network][id]["name"]

                    for admin_id in config.tg_bot.admin_ids:
                        await bot.send_message(chat_id=admin_id, text=f"{name_wallet} {network} {id}\n"
                                                                           f"{error}")
        del data[ip]
    logging.info(f"Data_end: {data}")   

    with open(path_save_file, "w") as file:
        json.dump(data, file)
        
