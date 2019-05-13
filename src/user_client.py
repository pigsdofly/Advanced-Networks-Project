import socket
from config import HOST, PORT
from utils import byte_encode

class UserClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect_ex((HOST, PORT))

    def send_data(self, out_string):
        out_string = 'ms' + out_string
        self.sock.sendall(byte_encode(out_string))

    def receive_data(self):
        data = self.sock.recv(1024)
        return data.decode("utf-8")
    
    def close_connection(self):
        self.sock.close()

if __name__ == '__main__':
    
    client = UserClient();
    while True:
        print(client.receive_data())
        out_str = input("")
        client.send_data(out_str)
        if out_str == "exit":
            client.close_connection()
            break
    print("Closed connection with server")
    
