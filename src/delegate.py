from bluepy import btle, thingy52
class DelegateHandler(btle.DefaultDelegate):
    def handleNotification( self, hnd, data ):
        pass

