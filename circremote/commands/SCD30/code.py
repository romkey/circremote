# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_scd30

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize SCD30
try:
    scd = adafruit_scd30.SCD30(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing SCD30: {e}")
    import sys
    sys.exit(1)

print("SCD30 CO2 Sensor")
print("=" * 20)

# Main reading loop
while True:
        if scd.data_available:
            # Read sensor values
            co2 = scd.CO2
            temperature = scd.temperature
            humidity = scd.relative_humidity
            
            # Display readings
            print(f"CO2: {co2:.1f} ppm")
            print(f"Temperature: {temperature:.1f}°C")
            print(f"Humidity: {humidity:.1f}%")
            print("-" * 30)
        
        time.sleep(30) 