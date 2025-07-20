# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_htu31d

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize HTU31
try:
    htu = adafruit_htu31d.HTU31D(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing HTU31: {e}")
    import sys
    sys.exit(1)

print("HTU31 Temperature & Humidity Sensor")
print("=" * 35)

# Main reading loop
while True:
        # Read sensor values
        temperature = htu.temperature
        humidity = htu.relative_humidity
        
        # Display readings
        print(f"Temperature: {temperature:.1f}°C")
        print(f"Humidity: {humidity:.1f}%")
        print("-" * 30)
        
        time.sleep(30) 