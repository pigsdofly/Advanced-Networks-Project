import socket 

def send_data(conn, data):
    conn.send(byte_encode(data))

def byte_encode(data):
    return bytes(data+'\n', 'utf8')
