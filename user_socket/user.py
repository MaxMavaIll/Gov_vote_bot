import socket, json
import os
from environs import Env
path_env = ".env" # os.path.abspath(".env")

def usr_server(data: dict ):
    env = Env()
    env.read_env(path_env)
    data = json.dumps(data)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((env.str("IP_SERVER"), 2000))

    sock.send(bytes(data, encoding="utf-8"))
