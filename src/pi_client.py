import socket
from config import HOST, PORT

class pi_client:
    def __init__(self, thingies):
        self.thingies = thingies
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self):
        self.sock.connect_ex((HOST, PORT))
        
