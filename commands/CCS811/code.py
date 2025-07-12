# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_ccs811

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize CCS811
try:
    ccs = adafruit_ccs811.CCS811(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing CCS811: {e}")
    import sys
    sys.exit(1)

print("CCS811 Air Quality Sensor")
print("=" * 25)

# Wait for sensor to be ready
while not ccs.data_ready:
    time.sleep(0.1)

# Main reading loop
while True:
    if ccs.data_ready:
        eco2 = ccs.eco2
        tvoc = ccs.tvoc
            
        print(f"eCO2: {eco2} ppm")
        print(f"TVOC: {tvoc} ppb")
        print("-" * 30)
        
        time.sleep(30)
