import socket
from config import HOST, PORT
from utils import send_data, byte_encode

class PiClient:
    def __init__(self, thingies):
        self.thingies = thingies
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self):
        example_temps = "pi[21, 23]"
        self.sock.connect_ex((HOST, PORT))
        # Receive the intro message from the server but don't display it
        data = self.sock.recv(1024)
        self.sock.sendall(byte_encode(example_temps))
        data = self.sock.recv(1024)
        print(repr(data))
        self.sock.sendall(byte_encode('exit'))
        
    def send_temps(self):
        
        pass

if __name__ == '__main__':
    client = PiClient([])
    client.connect()
