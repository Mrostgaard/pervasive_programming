#from umqtt import MQTTClient
from network import WLAN
import pycom
import socket
import time
import machine

wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()
for net in nets:
    if net.ssid == 'sensors':
        print('Network found!', end='')
        wlan.connect(net.ssid, auth=(net.sec, 'n0n53n53'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
            print('idle', end='')
        print('WLAN connection succeeded!')
        break

def http_get(url):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data: 
            print('print', end='')
        else:
            break
    s.close()
    

for cycles in range(10):
    http_get("http://training.itu.dk/receiver/receiver.php?MY_VALUE=123")