# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_si7021

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize Si7021
try:
    si7021 = adafruit_si7021.SI7021(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing Si7021: {e}")
    import sys
    sys.exit(1)

print("Si7021 Temperature & Humidity Sensor")
print("=" * 35)

# Main reading loop
while True:
        # Read sensor values
        temperature = si7021.temperature
        humidity = si7021.relative_humidity
        
        # Display readings
        print(f"Temperature: {temperature:.1f}°C")
        print(f"Humidity: {humidity:.1f}%")
        print("-" * 30)
        
        time.sleep(30) 