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
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    print(data)
                    print(data == byte_encode("lol"))
                    if data == byte_encode("lol"):
                        conn.send(byte_encode("haha"))
                    elif data == byte_encode("exit"):
                        s.close()
                        break
                    else:
                        conn.send(byte_encode("Not a recognised command"))
        finally:
            s.close()

def byte_encode(data):
    return bytes(data+'\n', 'utf8')

if __name__ == '__main__':
    open_server()
