from network import LoRa 
import struct 
import binascii 
import socket 

# Initialize LoRa in LORAWAN mode. 
lora = LoRa(mode=LoRa.LORAWAN) 

#Device Address 
dev_addr = struct.unpack(">l", binascii.unhexlify('260113A1'))[0] 
#Network Session Key 
nwk_swkey = binascii.unhexlify('603B1B5C207DC598BC53A9321A3433AA') 
#App Session Key 
app_swkey = binascii.unhexlify('21F1CFF87F5CB77941C9CFACEC736F98')


lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey)) 
# create a LoRa socket 
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW) 
# set the LoRaWAN data rate 
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 3) 
# make the socket non-blocking 
s.setblocking(False)