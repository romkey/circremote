# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_adt7410

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize ADT7410
try:
    adt = adafruit_adt7410.ADT7410(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing ADT7410: {e}")
    import sys
    sys.exit(1)

print("ADT7410 High-Accuracy Temperature Sensor")
print("=" * 40)

while True:
    temperature = adt.temperature
        
    print(f"Temperature: {temperature:.2f}°C")
    print("-" * 30)
        
    time.sleep(30)
