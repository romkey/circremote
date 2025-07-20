import time

import wifi
import socketpool

import adafruit_ntp

print(f"Connected! IP: { wifi.radio.ipv4_address }")

pool = socketpool.SocketPool(wifi.radio)
ntp = adafruit_ntp.NTP(pool, server="{{ server }}", tz_offset=0)
#ntp = adafruit_ntp.NTP(pool, tz_offset=0)

print("Fetching time from NTP...")
time.sleep(2)

current_time = ntp.datetime
print("Current UTC time:", current_time)
