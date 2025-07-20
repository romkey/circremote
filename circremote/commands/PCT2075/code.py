# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_pct2075

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize PCT2075
try:
    pct = adafruit_pct2075.PCT2075(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing PCT2075: {e}")
    import sys
    sys.exit(1)

print("PCT2075 Temperature Sensor")
print("=" * 25)

while True:
    temperature = pct.temperature
        
    print(f"Temperature: {temperature:.2f}°C")
    print("-" * 30)
        
    time.sleep(30)
