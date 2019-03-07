import config
import delegate
from bluepy import btle, thingy52

if __name__ == '__main__':
    thingy = thingy52.Thingy52(config.MAC_ADDRESS)

