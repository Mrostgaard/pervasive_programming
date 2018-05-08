import time
import utime
import machine
from network import WLAN
import urequests

import deepsleep

from machine import Pin
from onewire import DS18X20
from onewire import OneWire

## Setup the temperature sensor
adc = machine.ADC()
ow = OneWire(Pin('P11')) ## Use P!
temp = DS18X20(ow)

## Setup the WLAN connection
wlan = WLAN(mode=WLAN.STA)

nets = wlan.scan()
for net in nets:
    if net.ssid == 'sensors':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, 'n0n53n53'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break

while(True):
    print('Light: ' + str(photores()))
    time.sleep(1)
    print('Temp: ' + str(temp.read_temp_async()))
    time.sleep(1)
    temp.start_conversion()
    time.sleep(1)
    print(utime.localtime())

tmp =  str(temp.read_temp_async())
temp.start_conversion()
tmp =  str(temp.read_temp_async())
print('Temp: ' + tmp)

if tmp == "None":
    print("Temp is None")
    machine.deepsleep(18)

data = {"water_tmp": float(tmp)}

print(data)
#response = urequests.post('http://130.226.140.7:8086/mrom_jpip/', json=data)
#print(response.status_code)

response = urequests.post('http://130.226.140.7:1880/mrom/', json=data)
print("Wuhu")
print(response.text)
print("StatusCode: ", response.status_code)

response.close()

print('Going into deepsleep for 30 minutes')
machine.deepsleep(1800000)
    #machine.deepsleep(1800000)
