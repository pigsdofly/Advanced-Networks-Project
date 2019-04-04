import socket 
from enum import Enum

class SensorTypes(Enum):
    TEMPERATURE = 0
    PRESSURE = 1
    HUMID = 2
    GAS = 3
    BUTTON = 4


def byte_encode(data):
    newline = '\n'
    if data[-1] == '\n':
        newline = ''
    return bytes(data+newline, 'utf8')
