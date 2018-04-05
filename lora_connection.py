from network import LoRa
import socket
import time

# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORA, frequency=863000000)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(True)

while True:
    if s.recv(64) == b'Ping':
        s.send('Pong')
        print('hej')
    time.sleep(5)
