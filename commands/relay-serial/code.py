# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

import board
import busio
import time

RX_PIN = board.IO11

uart = busio.UART(tx=None, rx=RX_PIN, baudrate=115200, timeout=0.1)

print("Listening for serial data on RX...")

while True:
try:
    data = uart.read(1)
    if data:
        try:
except Exception as e:    print(f"Error initializing relay-serial: {e}")    import sys    sys.exit(1)            print(data.decode(), end='')
        except:
            print('X', end='')
#        print("Received:", data.decode(errors="ignore"))
    time.sleep(0.1)
