# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
from adafruit_ds248x import Adafruit_DS248x

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize DS2484
try:
    ds248x = Adafruit_DS248x(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing DS2484: {e}")
    import sys
    sys.exit(1)

print("DS2484 1-Wire Master Controller")
print("=" * 30)

while True:
    rom = bytearray(8)
    if not ds248x.onewire_search(rom):
        print("no devices found")
    else:
        print(f"device found {rom.hex()}")

        temperature = ds248x.ds18b20_temperature(rom)
        print(f"Temperature: {temperature:.2f} °C")
        
    print("-" * 30)
    time.sleep(10) 
