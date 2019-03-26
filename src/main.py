import config
import delegate
import socket
from bluepy import btle, thingy52

def add_thingies():
    thingies = []

    for addr in config.MAC_ADDRESS:
        thingy = thingy52.Thingy52(addr)
        thingy.setDelegate(delegate.DelegateHandler())
        thingies.append(thingy)

    return thingies
    

if __name__ == '__main__':
    try:
        thingies = add_thingies()
        while(True):
            for thingy in thingies:
                thingy.sound.enable()
                thingy.sound.configure(speaker_mode=0x03)
                thingy.sound.play_speaker_sample(5)
                thingy.waitForNotifications(timeout=10)
    finally:
        thingy.disconnect()
        del thingy
