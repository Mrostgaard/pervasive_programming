from network import WLAN
wlan.init(mode=WLAN.AP, ssid='PleaseHackMeLOPY', auth=(WLAN.WPA2,'yourPassword'),
channel=7, antenna=WLAN.INT_ANT)
