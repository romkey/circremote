# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_ens160

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize ENS160
try:
    ens = adafruit_ens160.ENS160(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing ENS160: {e}")
    import sys
    sys.exit(1)

print("ENS160 Air Quality Sensor")
print("=" * 25)

# Main reading loop
while True:
        # Read sensor values
        aqi = ens.AQI
        tvoc = ens.TVOC
        eco2 = ens.eCO2
        
        # Display readings
        print(f"Air Quality Index: {aqi}")
        print(f"TVOC: {tvoc:.1f} ppb")
        print(f"eCO2: {eco2:.1f} ppm")
        print("-" * 30)
        
        time.sleep(30) 