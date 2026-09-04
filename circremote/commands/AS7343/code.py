# SPDX-FileCopyrightText: 2026 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
from adafruit_as7343 import AS7343

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize AS7343
try:
    sensor = AS7343(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing AS7343: {e}")
    import sys
    sys.exit(1)

# Channel labels for the 18 values returned in the default CH18 SMUX mode
CHANNEL_LABELS = [
    "FZ  (450nm blue)",
    "FY  (555nm yellow-green)",
    "FXL (600nm orange)",
    "NIR (855nm near-IR)",
    "VIS_TL_0 (clear top-left, cycle 1)",
    "VIS_BR_0 (clear btm-right, cycle 1)",
    "F2  (425nm violet-blue)",
    "F3  (475nm blue-cyan)",
    "F4  (515nm green)",
    "F6  (640nm red)",
    "VIS_TL_1 (clear top-left, cycle 2)",
    "VIS_BR_1 (clear btm-right, cycle 2)",
    "F1  (405nm violet)",
    "F7  (690nm deep red)",
    "F8  (745nm near-IR edge)",
    "F5  (550nm green-yellow)",
    "VIS_TL_2 (clear top-left, cycle 3)",
    "VIS_BR_2 (clear btm-right, cycle 3)",
]

print("AS7343 14-Channel Spectral Sensor")
print("=" * 40)

# Display sensor information
try:
    print(f"Part ID: 0x{sensor.part_id:02X}")
    print(f"Revision ID: 0x{sensor.revision_id:02X}")
except Exception:
    pass
print(f"Integration Time: {sensor.integration_time_ms:.2f} ms")
print(f"ASTEP: {sensor.astep}")
print()

# Main reading loop
while True:
    try:
        readings = sensor.all_channels

        print("Channel Readings:")
        for label, value in zip(CHANNEL_LABELS, readings):
            print(f"  {label}: {value}")
        print("-" * 40)

    except Exception as e:
        print(f"Error reading sensor data: {e}")
        print("-" * 40)

    time.sleep(1)
