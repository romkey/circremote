# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_hdc302x

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize HDC3022
try:
    hdc3022 = adafruit_hdc302x.HDC302x(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing HDC3022: {e}")
    import sys
    sys.exit(1)

print("HDC3022 Temperature & Humidity Sensor")
print("=" * 40)

while True:
    temp = hdc3022.temperature
    humidity = hdc3022.relative_humidity
    print(f"Temperature: {temp:.1f}°C")
    print(f"Humidity: {humidity:.1f}%")
        
    time.sleep(30)
