import pycom
from network import WLAN
import socket
import time
import ssl
pycom.heartbeat(False)

### Connect to WiFi ###
def connect_to_wifi():
    wlan = WLAN(mode=WLAN.STA)
    if wlan.isconnected(): return

    nets = wlan.scan()
    for net in nets:
        if net.ssid == 'sensors':
            print('Network found!')
            wlan.connect(net.ssid, auth=(net.sec, 'n0n53n53'), timeout=5000)
            while not wlan.isconnected():
                machine.idle() # save power while waiting
            print('WLAN connection succeeded!')
            break

### Perform HTTP GET for url ###
def http_get(url):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(500)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()

# Connect to WiFi
connect_to_wifi()

# Fetch every 60th second
while True:

    # Fetch OpenWeatherMap API
    print("\n\n............... FETCHING data ...............")
    http_get("http://api.openweathermap.org/data/2.5/weather?q=Copenhagen&appid=338e9d277c096486440c0407567b4b78")
    print("\n\n............... FETCHED DATA ...............")

    #Put in idle here, when finished fetching

    time.sleep(60)
