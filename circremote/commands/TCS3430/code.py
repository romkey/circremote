# SPDX-FileCopyrightText: 2026 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
from adafruit_tcs3430 import TCS3430, ALSGain

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize TCS3430
try:
    sensor = TCS3430(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing TCS3430: {e}")
    import sys
    sys.exit(1)

print("TCS3430 XYZ Tristimulus Color Sensor")
print("=" * 40)

# Moderate gain and integration time suitable for indoor lighting
sensor.als_gain = ALSGain.GAIN_16X
sensor.integration_time = 100.0

# Display sensor information
print(f"Chip ID: 0x{sensor.chip_id:02X}")
print(f"Revision ID: 0x{sensor.rev_id:02X}")
print(f"ALS Gain: {ALSGain.get_name(sensor.als_gain)}")
print(f"Integration Time: {sensor.integration_time:.2f} ms")
print()

# Main reading loop
while True:
    try:
        x, y, z, ir1 = sensor.channels

        print(f"X: {x}")
        print(f"Y: {y}")
        print(f"Z: {z}")
        print(f"IR1: {ir1}")

        # CIE 1931 chromaticity coordinates
        total = x + y + z
        if total > 0:
            cx = x / total
            cy = y / total
            print(f"Chromaticity: x={cx:.4f} y={cy:.4f}")

        if sensor.als_saturated:
            print("ALS saturated - reduce gain or integration time")
            sensor.clear_als_saturated()

        print("-" * 30)

    except Exception as e:
        print(f"Error reading sensor data: {e}")
        print("-" * 30)

    time.sleep(1)
