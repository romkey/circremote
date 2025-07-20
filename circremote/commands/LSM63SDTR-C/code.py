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

# Initialize LSM63SDTR-C
try:
    lsm = adafruit_lsm6ds.LSM6DS33(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing LSM63SDTR-C: {e}")
    import sys
    sys.exit(1)

print("LSM63SDTR-C 6-Axis IMU")
print("=" * 25)

# Main reading loop
while True:
        # Read accelerometer values
        accel_x, accel_y, accel_z = lsm.acceleration
        
        # Read gyroscope values
        gyro_x, gyro_y, gyro_z = lsm.gyro
        
        # Display readings
        print(f"Accelerometer (m/s²):")
        print(f"  X: {accel_x:.2f}")
        print(f"  Y: {accel_y:.2f}")
        print(f"  Z: {accel_z:.2f}")
        print(f"Gyroscope (rad/s):")
        print(f"  X: {gyro_x:.2f}")
        print(f"  Y: {gyro_y:.2f}")
        print(f"  Z: {gyro_z:.2f}")
        print("-" * 30)
        
        time.sleep(1) 