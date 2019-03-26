import config
import delegate
from bluepy import btle, thingy52

if __name__ == '__main__':
    try:
        thingy = thingy52.Thingy52(config.MAC_ADDRESS)
        thingy.setDelegate(delegate.DelegateHandler())
        while(True):
            thingy.waitForNotifications(timeout=10)
    finally:
        thingy.disconnect()
        del thingy
