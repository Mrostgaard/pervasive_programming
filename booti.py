import os
import pycom
from machine import UART
from network import WLAN

uart = UART(0, 115200)
os.dupterm(uart)
pycom.heartbeat(False)

wlan = WLAN()
wlan.deinit()
