import time
from machine import I2C
from struct import unpack
class Chirp:
	def __init__(self, address):
		self.address = address

	def change_adress(self, new_adress):
		i2c.writeto_mem(self.address, 1, bytes([new_adress]))

if __name__ == '__main__':
	i2c = I2C(0, I2C.MASTER, baudrate=10000)
	print('Current active addresses: '+str(i2c.scan()))
	addr = i2c.scan()[0]
	print('Chosen adress: '+str(addr))
	chirp = Chirp(addr)
	adress_upd = int(input('enter a new adress: (between 1 and 127)'))
	print(type(adress_upd))
	chirp.change_adress(adress_upd)
