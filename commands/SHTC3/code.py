# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_shtc3

print("SHTC3 Temperature & Humidity Sensor")
print("=" * 40)

# Initialize I2C bus
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize SHTC3 sensor
try:
    shtc3 = adafruit_shtc3.SHTC3(i2c)
except Exception as e:
    print(f"Error initializing SHTC3: {e}")
    import sys
    sys.exit(1)

print("\nStarting temperature and humidity measurements...")
print("Readings:")

while True:
    temperature, humidity = shtc3.measurements
    print(f"Temperature: {temperature:.2f} °C")
    print(f"Humidity: {humidity:.2f} %")
    print("-" * 30)
    time.sleep(30)
