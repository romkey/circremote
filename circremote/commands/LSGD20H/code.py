# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_lsm6ds

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize LSGD20H
try:
    lsm = adafruit_lsm6ds.LSGD20H(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing LSGD20H: {e}")
    import sys
    sys.exit(1)

print("LSGD20H 3-Axis Gyroscope")
print("=" * 25)

# Main reading loop
while True:
        # Read gyroscope values
        gyro_x, gyro_y, gyro_z = lsm.gyro
        
        # Display readings
        print(f"X: {gyro_x:.2f} rad/s")
        print(f"Y: {gyro_y:.2f} rad/s")
        print(f"Z: {gyro_z:.2f} rad/s")
        print("-" * 30)
        
        time.sleep(1) 