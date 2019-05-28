''' Client for the raspberry pi, reads temperature data from local thingies and updates temperature data on the server with it'''
import socket
import thing
import time
from bluepy import thingy52
from config import TARGET, PORT, MAC_ADDRESS
from utils import byte_encode, SensorTypes

class PiClient:
    def __init__(self):
        self.thingies = self.fill_thingies()


    def make_socket(self):
        sock_type = socket.AF_INET
        if ':' in TARGET:
            sock_type = socket.AF_INET6

        self.sock = socket.socket(sock_type, socket.SOCK_STREAM)
  
    def connect(self):
        example_temps = self.get_temps()
        self.make_socket()
        self.sock.connect_ex((TARGET, PORT))
        # Receive the intro message from the server but don't display it
        try:
            data = self.sock.recv(1024)
        
        except:
            pass

        self.sock.send(byte_encode(example_temps))
        try:
            data = self.sock.recv(1024)
        except:
            pass

        self.sock.send(byte_encode('msexit\n'))
        self.sock.close()
        self.disable_sensors()
        

    def disable_sensors(self):
        for device in self.thingies:
           device.environment.set_temperature_notification(False)
           device.environment.set_pressure_notification(False)
           device.environment.set_humidity_notification(False)

    def get_temps(self):
        device_info = []
        for device in self.thingies:
            dev_dict = {}
            dev_dict['name'] = thing.getName(device)
            print(dev_dict['name'])

            thing.selectSensor(SensorTypes.TEMPERATURE, device)
            thing.selectSensor(SensorTypes.HUMID, device)
            thing.selectSensor(SensorTypes.PRESSURE, device)


            device.waitForNotifications(2)

            #Get sensor data from the delegate
            dev_temp = device.delegate.temps
            dev_humidity = device.delegate.humidity
            dev_pressure = device.delegate.pressure

            rounded_pressure = '{}.{}'.format(int(dev_pressure[:-2],16), int(dev_temp[-2:], 16))
            rounded_temp = '{}.{}'.format(int(dev_temp[:-2], 16), int(dev_temp[-2:], 16))
            dev_dict['temp'] = rounded_temp
            dev_dict['humidity'] = dev_humidity
            dev_dict['pressure'] = rounded_pressure
            device_info.append(dev_dict)

        dev_string = 'pi'+str(device_info)
        print(dev_string)
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
   
    while True:
        client.connect()
        time.sleep(5)
