import socket
import thing
from bluepy import thingy52
from config import HOST, PORT, MAC_ADDRESS
from utils import send_data, byte_encode, SensorTypes

class PiClient:
    def __init__(self):
        self.thingies = self.fill_thingies()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self):
        example_temps = self.get_temps()
        self.sock.connect_ex((HOST, PORT))
        # Receive the intro message from the server but don't display it
        data = self.sock.recv(1024)
        self.sock.sendall(byte_encode(example_temps))
        data = self.sock.recv(1024)
        print(repr(data))
        self.sock.sendall(byte_encode('exit'))
        self.sock.close()
        
    def get_temps(self):
        temp_string = "pi[21, 23]"
        for device in self.thingies:
            thing.selectSensor(SensorTypes.TEMPERATURE, device)
            rounded_temp = ""
            while len(rounded_temp) < 5:
                device.waitForNotifications(2)
                #Get temperature information from the delegate
                #I hate this
                rounded_temp  = str(device.delegate.temps)
            
            rounded_temp = rounded_temp[0:2]
            print(rounded_temp)
            temp_string = "pi"+"["+str(rounded_temp)+"]"
            
            print(device.delegate.temps)
        return temp_string

    def fill_thingies(self):
        thingies = []

        for addr in MAC_ADDRESS:
            thingy = thingy52.Thingy52(addr)
            thingy.setDelegate(thing.NewDelegate())
            thingies.append(thingy)

        return thingies
if __name__ == '__main__':
    
    client = PiClient()
    client.connect()
