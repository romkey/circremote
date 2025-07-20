# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_lis3dh

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize LIS3DH
try:
    lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing LIS3DH: {e}")
    import sys
    sys.exit(1)

print("LIS3DH Accelerometer")
print("=" * 25)

# Display sensor information
print(f"Range: {lis3dh.range}")
print(f"Data Rate: {lis3dh.data_rate}")
print(f"Mode: {lis3dh.mode}")
print()

# Main reading loop
while True:
    # Read accelerometer data
    x, y, z = lis3dh.acceleration
    
    print(f"Acceleration (m/s²): X={x:.2f}, Y={y:.2f}, Z={z:.2f}")
    print("-" * 30)
    
    time.sleep(1)