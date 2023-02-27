import socket, json
import os
from environs import Env
import logging
path_env = ".env" # os.path.abspath(".env")

def usr_server(data: dict ):
    env = Env()
    env.read_env(path_env)
    
    logging.info("I send json file on this server: {}".format(env.str("IP_SERVER")))
    logging.info(f"{data}\n\n\n")
    data = json.dumps(data)
    logging.info(data)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("135.181.138.161", 2000))

    sock.sendall(data.encode())


# usr_server({"Menu": 0})