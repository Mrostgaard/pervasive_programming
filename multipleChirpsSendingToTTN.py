import time
import binascii
import socket
from network import LoRa
from machine import I2C
from machine import Pin
from struct import unpack
from onewire import DS18X20
from onewire import OneWire

class Chirp:
	def __init__(self, address):
		global i2c
		self.address = address

	def get_reg(self, reg):
		val = unpack('<H', (i2c.readfrom_mem(self.address, reg, 2)))[0]
		return (val >> 8) + ((val & 0xFF) << 8)

	def moist(self):
		return self.get_reg(0)

	def temp(self):
		return self.get_reg(5)

	def light(self):
		i2c.writeto(self.address, '\x03')
		time.sleep(3)
		return self.get_reg(4)

class LoRaNetwork:
    def __init__(self):
        global chirp_list
        global temp

        # Initialize LoRaWAN radio
        self.lora = LoRa(mode=LoRa.LORAWAN)

        # Set network keys
        app_eui = binascii.unhexlify('70B3D57EF0003F19')
        app_key = binascii.unhexlify('C2CCD5500390D439888D8EB38C0249FC')

        # Join the network
        self.lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

        # Loop until joined
        while not self.lora.has_joined():
            print('Not joined yet...')
            time.sleep(2)

        print('Joined')

        self.s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        self.s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
        self.s.setblocking(True)
        self.bytesarraytemp = bytearray((len(chirp_list) * 3)+1)

    def convertbytes(self, data):
        for i in range(0, 13):
            self.bytesarraytemp[i] = data[i]
        return self.bytesarraytemp

    def normalizedata(self, oldval, oldmin, oldmax):
        oldRange = oldmax - oldmin
        newRange = 255 - 0
        return (((oldval - oldmin) * newRange) / oldRange) + 0

    def preparedata(self, data):
        data[0] = int(data[0]*2)
        data[1] = int(self.normalizedata(data[1], 245, 613)) #245 min 613 max
        data[2] = int(self.normalizedata(data[2], 65535, 0)) #65535 min 0 max
        return data

    def senddata(self):
        dataList = []
        for chirp in chirp_list:
            tempList = []
            tempList.append(float(chirp.temp()/10))
            tempList.append(chirp.moist())
            tempList.append(chirp.light())
            tempList = self.preparedata(tempList)
            dataList.extend(tempList)
        temp.start_conversion()
        waterTemp = temp.read_temp_async()
        dataList.append(int(temp.read_temp_async()*2))
        print(dataList)
        self.s.send(self.convertbytes(dataList))

if __name__ == '__main__':
    i2c = I2C(0, I2C.MASTER, baudrate=10000)
    addresses = i2c.scan()
    chirp_list = []
    for a in addresses:
        chirp_list.append(Chirp(a))

    ow = OneWire(Pin('P11'))
    temp = DS18X20(ow)

    lora = LoRaNetwork()

    while(True):
        lora.senddata()
        time.sleep(60)
