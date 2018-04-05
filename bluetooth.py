from network import Bluetooth
from struct import unpack
import pycom

bluetooth = Bluetooth()
bluetooth.set_advertisement(name='Light', service_uuid=b'setLight12345678')

def conn_cb (bt_o):
    events = bt_o.events()
    if  events & Bluetooth.CLIENT_CONNECTED:
        print("Client connected")
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        print("Client disconnected")


bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=conn_cb)

bluetooth.advertise(True)

srv1 = bluetooth.service(uuid=b'setLight12345678', isprimary=True)

chr1 = srv1.characteristic(uuid=b'asetLight1234567', value=5)

char1_read_counter = 0
def char1_cb_handler(chr):
    global char1_read_counter
    char1_read_counter += 1

    events = chr.events()
    value = unpack("<H", chr.value())[0]
    if  events & Bluetooth.CHAR_WRITE_EVENT:
        pycom.rgbled(0x007f00)
        print("Write request with value = {}".format(value))
    else:
        if char1_read_counter < 3:
            print('Read request on char 1')
        else:
            return 'ABC DEF'

char1_cb = chr1.callback(trigger=Bluetooth.CHAR_WRITE_EVENT | Bluetooth.CHAR_READ_EVENT, handler=char1_cb_handler)