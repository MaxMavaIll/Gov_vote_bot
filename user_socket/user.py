import socket, json
from environs import Env


def usr_server(data: dict ):
    env = Env()
    data = json.dumps(data)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((env.str("IP_SERVER"), 2000))

    sock.send(bytes(data, encoding="utf-8"))
