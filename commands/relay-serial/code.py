# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

import board
import busio
import time

uart = busio.UART(tx=None, rx={{ rx_pin }}, baudrate=115200, timeout=0.1)

print("Listening for serial data on RX...")

while True:
    try:
        data = uart.read(1)
        if data:
            try:
                print(data.decode(), end='')
            except:
                print('X', end='')
        time.sleep(0.1)
    except Exception as e:
        print(f"Error reading serial data: {e}")
        time.sleep(1)
