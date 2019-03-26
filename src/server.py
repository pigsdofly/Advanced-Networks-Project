import socket
from config import HOST, PORT

def open_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        try:
            with conn:
                print('Connected by', addr)
                conn.send(byte_encode("Welcome to the thermostat of the future! (not)"))
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    print(data)
                    if data == byte_encode("lol"):
                        send_data(conn, "lol")
                    elif data == byte_encode("temperature"):
                        send_data(conn, "coming soon")
                    elif data == byte_encode("devices"):
                        send_data(conn, "coming soon")
                    elif data == byte_encode("help"):
                        send_data(conn, "Current commands:\n\ttemperature: show temperature\n\tdevices: show connected devices\n\texit: exit")
                    elif data == byte_encode("exit"):
                        send_data(conn, "closing connection")
                        s.close()
                        break
                    else:
                        conn.send(byte_encode("Not a recognised command"))
        finally:
            s.close()

def send_data(conn, data):
    conn.send(byte_encode(data))

def byte_encode(data):
    return bytes(data+'\n', 'utf8')

if __name__ == '__main__':
    open_server()
