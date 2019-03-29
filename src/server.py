import socket
import ast
from config import HOST, PORT
from utils import send_data, byte_encode

class Server:
    current_temps = []
    current_devices = []

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((HOST, PORT))
        self.s.listen(1)
        print("Server running on port "+str(PORT))

    def open_server(self):
        try:
            while True:
                conn, addr = self.s.accept()
                self.handle_data(conn, addr)

        finally:
            self.s.close()

    def handle_data(self, conn, addr):
        print('Connected by', addr)
        conn.send(byte_encode("Welcome to the thermostat of the future! (not)"))
        while True:
#            try:
            data = conn.recv(1024)
            if not data:
                break
            print(data[0:2])
            if data[0:2] == bytes("pi",'utf8'):
                clean_data = data[2:-1].decode('utf-8')
                clean_data = ast.literal_eval(clean_data)
                self.current_temps = clean_data
                send_data(conn, "data received")
                print("Temps are now: "+str(self.current_temps[0]))
            else:
                if data == byte_encode("lol"):
                    send_data(conn, "lol")
                elif data == byte_encode("temperature"):
                    message = "The current temperatures are "+str(self.current_temps)
                    send_data(conn, message)
                elif data == byte_encode("devices"):
                    send_data(conn, "coming soon")
                elif data == byte_encode("help"):
                    send_data(conn, "Current commands:\n\ttemperature: show temperature\n\tdevices: show connected devices\n\texit: exit")
                elif data == byte_encode("exit"):
                    send_data(conn, "closing connection")
                    conn.close()
                    break
                else:
                    conn.send(byte_encode("Not a recognised command"))
 #           except:
   #             conn.close()
  #              break

if __name__ == '__main__':
    server = Server()
    server.open_server()
