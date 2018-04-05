import machine
from network import WLAN
wlan = WLAN(mode=WLAN.STA)

nets = wlan.scan()
for net in nets:
    if net.ssid == 'sensors':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, 'n0n53n53'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
            print('idle')
        print('WLAN connection succeeded!')
        break