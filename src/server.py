import socket
import selectors
import ast
import types
from config import HOST, PORT
from utils import byte_encode

class Server:
    current_temps = []
    current_devices = []

    def __init__(self):
        self.sel = selectors.DefaultSelector()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((HOST, PORT))
        self.s.listen()
        
        print("Server running on port "+str(PORT))
        self.s.setblocking(False)
        self.sel.register(self.s, selectors.EVENT_READ, data=None)

    def open_server(self):
        try:
            while True:
                events = self.sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        self.handle_data(key, mask)
            #while True:
             #   conn, addr = self.s.accept()
             #   self.handle_data(conn, addr)

        finally:
            self.s.close()

    def accept_wrapper(self, sock):
        conn, addr = sock.accept()
        print("Accepted connection from ", addr)
        conn.setblocking(False)
        conn.send(byte_encode("Welcome to the thermostat of the future! (Not)\nTo see list of commands, type 'help'"))
        data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)


    def handle_data(self, key, mask):
        conn = key.fileobj
        key_data = key.data

        if mask & selectors.EVENT_READ:
            data = conn.recv(1024)
            if data:
                key_data.inb = data
                if data[0:2] == bytes("pi",'utf8'):
                    clean_data = data[2:-1].decode('utf-8')
                    clean_data = ast.literal_eval(clean_data)
                    self.current_temps = clean_data
                    print(self.get_temp_info())

            else:
                self.sel.unregister(conn)
                conn.close()

        if mask & selectors.EVENT_WRITE:
            data = key_data.inb
            if data[0:2] == bytes("ms","utf8"):
                print(data)
                data = data[2:]
                    
                if data == byte_encode("lol"):
                    self.send_data(conn, "lol", key_data)
                elif data == byte_encode("temperature"):
                    self.send_data(conn, self.get_temp_info(), key_data)
                elif data == byte_encode("devices"):
                    self.send_data(conn, self.get_devices(), key_data)
                elif data == byte_encode("help"):
                    self.send_data(conn, "Current commands:\n\ttemperature: show temperature\n\tdevices: show connected devices\n\texit: exit", key_data)
                elif data == byte_encode("exit"):
                    print("Closed connection")
                    self.sel.unregister(conn)
                    conn.close()
                elif data != b'':
                    self.send_data(conn, "Not a recognised command", key_data)
            
            elif data != b'':
                self.send_data(conn, "Not a recognised command", key_data)
    
    def send_data(self, conn, message, data):
        b_message = byte_encode(message)
        sent = conn.send(b_message)
        data.inb = b''

    def get_devices(self):
        if len(self.current_temps) == 0:
            return "No device info available"
        else:
            ret_str = "Currently connected devices:\n "
            for device in self.current_temps:
                ret_str += device['name'] + '\n'
            return ret_str


    def get_temp_info(self):
        if len(self.current_temps) == 0:
            return "No device info available"
        else:
            ret_str = ""
            for device in self.current_temps:
                ret_str += "The temperature near "+ device['name'] + " is: "+device['temp'] + '\n'
            return ret_str

if __name__ == '__main__':
    server = Server()
    server.open_server()
