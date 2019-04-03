import socket 
from enum import Enum

class SensorTypes(Enum):
    TEMPERATURE = 0
    PRESSURE = 1
    HUMID = 2
    GAS = 3
    BUTTON = 4

def send_data(conn, data):
    conn.send(byte_encode(data))

def byte_encode(data):
    return bytes(data+'\n', 'utf8')
