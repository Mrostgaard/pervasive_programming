import time
import utime
import machine
import urequests
import deepsleep

from network import WLAN
from machine import Pin
from onewire import DS18X20
from onewire import OneWire

## Setup the temperature sensor
adc = machine.ADC()
ow = OneWire(Pin('P11')) ## Use P!
temp = DS18X20(ow)

## Connect to the Wi-Fi
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

tmp =  str(temp.read_temp_async())
temp.start_conversion()

#print("Tmp: ", float(tmp))

if tmp == "None":
    tmp = 0.0

data = {"water_tmp": float(tmp)}
response = urequests.post('http://130.226.140.7:1880/mrom/', json=data)
#print("StatusCode: ", response.status_code)
response.close()

print('Going into deepsleep for 30 minutes')
machine.deepsleep(1800000) #1800000
