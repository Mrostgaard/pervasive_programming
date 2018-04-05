import time
import utime
from machine import Pin
import machine
from onewire import DS18X20
from onewire import OneWire

adc = machine.ADC()
ow = OneWire(Pin('P11'))
temp = DS18X20(ow)
photores = adc.channel(pin='G3')

while(True):
    print('Light: ' + str(photores()))
    time.sleep(1)
    print('Temp: ' + str(temp.read_temp_async()))
    time.sleep(1)
    temp.start_conversion()
    time.sleep(1)
    print(utime.localtime())
