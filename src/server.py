import socket
from config import HOST, PORT

class Server:

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((HOST, PORT))
        self.s.listen(1)
        self.s.settimeout(30)

    def open_server(self):
        try:
            while True:
                conn, addr = self.s.accept()
                with conn:
                    print('Connected by', addr)
                    conn.send(self.byte_encode("Welcome to the thermostat of the future! (not)"))
                    while True:
                        try:
                            data = conn.recv(1024)
                            if not data:
                                break
                            print(data)
                            if data == self.byte_encode("lol"):
                                self.send_data(conn, "lol")
                            elif data == self.byte_encode("temperature"):
                                self.send_data(conn, "coming soon")
                            elif data == self.byte_encode("devices"):
                                self.send_data(conn, "coming soon")
                            elif data == self.byte_encode("help"):
                                self.send_data(conn, "Current commands:\n\ttemperature: show temperature\n\tdevices: show connected devices\n\texit: exit")
                            elif data == self.byte_encode("exit"):
                                self.send_data(conn, "closing connection")
                                conn.close()
                                break
                            else:
                                conn.send(self.byte_encode("Not a recognised command"))
                        except:
                            conn.close()

        finally:
            self.s.close()

    def send_data(self, conn, data):
        conn.send(self.byte_encode(data))

    def byte_encode(self, data):
        return bytes(data+'\n', 'utf8')

if __name__ == '__main__':
    server = Server()
    server.open_server()
