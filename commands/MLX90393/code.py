# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_mlx90393

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize MLX90393
try:
    mlx = adafruit_mlx90393.MLX90393(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing MLX90393: {e}")
    import sys
    sys.exit(1)

print("MLX90393 3-Axis Magnetometer")
print("=" * 30)

# Main reading loop
while True:
        # Read magnetometer values
        mag_x, mag_y, mag_z = mlx.magnetic
        
        # Display readings
        print(f"X: {mag_x:.2f} µT")
        print(f"Y: {mag_y:.2f} µT")
        print(f"Z: {mag_z:.2f} µT")
        print("-" * 30)
        
        time.sleep(1) 