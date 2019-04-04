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
        self.sock.sendall(byte_encode('exit'))
        self.sock.close()
        
    def get_temps(self):
        device_info = []
        for device in self.thingies:
            dev_dict = {}
            dev_dict['name'] = thing.getName(device)
            print(dev_dict['name'])

            thing.selectSensor(SensorTypes.TEMPERATURE, device)
            rounded_temp = ""
            device.waitForNotifications(2)
            #Get temperature information from the delegate
            t = device.delegate.temps
            rounded_temp  = '{}.{}'.format(int(t[:-2],16),int(t[-2:],16))
            dev_dict['temp'] = rounded_temp
            device_info.append(dev_dict)
            
        dev_string = 'pi'+str(device_info)
        print (dev_string)
        return dev_string

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
