import socketserver
import sys
import json
import logging as log


path_data_file = "data/pack_for_send.json"

def write_dict(data: dict):
    with open(path_data_file, "w") as file:
        json.dump(data, file)

class EchoHandler(socketserver.BaseRequestHandler):
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
    
if __name__ == "__main__":
    log.basicConfig(
        level=log.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )

    with socketserver.TCPServer(('', 9416), EchoHandler) as server:
        server.serve_forever()
