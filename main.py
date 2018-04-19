import time
import utime
import machine
from network import WLAN
import urequests

from machine import Pin
from onewire import DS18X20
from onewire import OneWire

## Setup the temperature sensor
adc = machine.ADC()
ow = OneWire(Pin('P11')) ## Use P!
temp = DS18X20(ow)
photores = adc.channel(pin='G3') ## Light resister delet


wlan = WLAN(mode=WLAN.STA)

nets = wlan.scan()
for net in nets:
    if net.ssid == 'iPhone':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, '12345678'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break
temp.start_conversion()

while(True):

    print('Light: ' + str(photores()))
    time.sleep(1)
    #tmp =  str(temp.read_temp_async())
    print('Temp: ' + tmp)
    time.sleep(1)
    temp.start_conversion()
    tmp =  str(temp.read_temp_async())
    time.sleep(1)

    data = {"water_tmp": tmp}
    response = urequests.post('http://130.226.140.7:1880/mrom/', json=data)
    print(response.text)
    print("StatusCode: ", response.status_code)
    time.sleep(1)
    response.close()
