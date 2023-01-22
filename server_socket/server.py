import socketserver
import sys
import json, logging



path_data_file = "data/pack_for_send.json"

def write_dict(data: dict):
    with open(path_data_file, "w") as file:
        json.dump(data, file)

class EchoHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = {}
        data_with_message = self.request.recv(1024).strip()
        data[self.client_address[0]] = json.loads(data_with_message.decode("utf-8"))
        logging.info("Address: {}".format(self.client_address[0]))
        logging.info("Data: {}".format(data_with_message.decode("utf-8")))
        write_dict(data)
        # socket.sendto()
    
if __name__ == "__main__":
    with socketserver.TCPServer(('localhost', 2000), EchoHandler) as server:
        server.serve_forever()
