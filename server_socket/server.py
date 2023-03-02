import socketserver
import sys
import json
import logging as log

from environs import Env

env = Env()
env.read_env(".env")

path_data_file = "data/pack_for_send.json"

def write_dict(data: dict):
    with open(path_data_file, "w") as file:
        json.dump(data, file)

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        with open(path_data_file, "r") as file:
            data = json.load(file)

        data_with_message = b""
        while True:
            chunk = self.request.recv(1024)
            data_with_message += chunk
            if len(chunk) < 1024:
                break
        data_with_message = data_with_message.decode()
        data[self.client_address[0]] = json.loads(data_with_message)
        log.info("Address: {}".format(self.client_address[0]))
        log.info("Data: {}".format(data_with_message))
        write_dict(data)
        # socket.sendto()

class CheckIpTCPServer(socketserver.TCPServer):
    # Забороняємо з'єднання з недозволених IP-адрес
    def verify_request(self, request, client_address):
        

        if client_address[0] in list(map(str, env.list("ALLOWED_IPS"))):
            return True
        else:
            log.info(f"This address wanted to connect with server {client_address[0]}\nPermission denied!")
            data_with_message = b""
            while True:
                chunk = request.recv(1024)
                data_with_message += chunk
                if len(chunk) < 1024:
                    break
            log.info(f'Data: {data_with_message}')
            return False

    
if __name__ == "__main__":
    log.basicConfig(
        level=log.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    log.info("Start Server")

    with CheckIpTCPServer(('', env.int("PORT")), MyTCPHandler) as server:
        server.serve_forever()
