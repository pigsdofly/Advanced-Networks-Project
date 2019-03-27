from bluepy import btle, thingy52
import binascii
import time

MAC_ADDRESS = 'DF:6F:CF:05:BA:72'

print ('# Creating new delegate class to handle notifications...')


class NewDelegate(btle.DefaultDelegate):

	def handleNotification(self, hnd, data):
		if hnd == thingy52.e_temperature_handle:
			data = int.from_bytes(data, byteorder='little')
			print ('Notification: Temperature received: '.data)
		if hnd == thingy52.ui_button_handle:
			data = int.from_bytes(data, byteorder='little')
			if data == 1:
				press = 'Button pressed'
			if data == 0:
				press ='Button Released'
			print ('Notification: Button recieved: ' . press)
		if hnd == thingy52.e_humidity_handle:
			data = int.from_bytes(data, byteorder='little')
			print('Notification: pressure recieved: ' .data)
		if hnd == thingy52.e_pressure_handle:
			data = int.from_bytes(data, byteorder='little')
			print('Notification: pressure recieved: ' .data)
		if hnd == thingy52.e_gas_handle:
			data = int.from_bytes(data, byteorder='little')
			print('Notification: gas recieved: ' .data)

#print ('# Connecting to Thingy with address {}...'.format(MAC_ADDRESS))
thingy = thingy52.Thingy52(MAC_ADDRESS)

# print("# Setting notification handler to default handler...")
# thingy.setDelegate(thingy52.MyDelegate())

print ('# Setting notification handler to new handler...')
thingy.setDelegate(NewDelegate())



# enable correct notifications depending on what is asked for?
# print notification for all thingies 

number = 0
#take raspberry pie command to find correct one e.g. temp gas pressure humid
#listen for command all the time 
#call disable at start of loop then enable correct notification
if number == 0:
	print ('# Configuring and enabling temperature notification...')
	thingy.environment.enable()
	thingy.environment.configure(temp_int=1000)
	thingy.environment.set_temperature_notification(True)


if number == 1:
	thingy.enviroment.configure(press_int=1000)
	thingy.enviroment.set_pressure_notification(True)

if number == 2:
	thingy.enviroment.configure(humid_int=1000)
	thingy.enviroment.set_humidity_notification(True)

if number == 3:
	thingy.enviroment.configure(gas_mode_int=1)
	thingy.enviroment.set_gas_notification(True)

if number == 4:
	thingy.ui.enable()
	thingy.ui.set_btn_notification(True)


while True:

	thingy.waitForNotifications(2)

	time.sleep(60)
thingy.disconnect()
