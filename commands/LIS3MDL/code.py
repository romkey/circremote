# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_lis3mdl

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize LIS3MDL
try:
    lis3mdl = adafruit_lis3mdl.LIS3MDL(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing LIS3MDL: {e}")
    import sys
    sys.exit(1)

print("LIS3MDL Magnetometer")
print("=" * 25)

# Display sensor information
print(f"Data Rate: {lis3mdl.data_rate}")
print(f"Range: {lis3mdl.range}")
print(f"Mode: {lis3mdl.mode}")
print()

# Main reading loop
while True:
        mag_x, mag_y, mag_z = lis3mdl.magnetic
        temp = lis3mdl.temperature
        
        print(f"Magnetic X: {mag_x:.2f} μT")
        print(f"Magnetic Y: {mag_y:.2f} μT")
        print(f"Magnetic Z: {mag_z:.2f} μT")
        print(f"Temperature: {temp:.1f}°C")
        print("-" * 30)
        
        time.sleep(30)