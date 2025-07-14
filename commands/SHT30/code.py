# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_sht31d

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize SHT30
try:
    sht30 = adafruit_sht31d.SHT31D(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing SHT30: {e}")
    import sys
    sys.exit(1)

print("SHT30 Temperature & Humidity Sensor")
print("=" * 40)

# Display sensor information
print(f"Heater: {sht30.heater}")
print(f"Status: {sht30.status}")
print(f"Reset Status: {sht30.reset_status}")
print()

# Main reading loop
while True:
        temp = sht30.temperature
        humidity = sht30.relative_humidity
        
        print(f"Temperature: {temp:.1f}°C")
        print(f"Humidity: {humidity:.1f}%")
        print("-" * 30)
        
        time.sleep(30)