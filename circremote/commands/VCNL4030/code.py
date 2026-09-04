# SPDX-FileCopyrightText: 2026 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
from adafruit_vcnl4030 import VCNL4030

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize VCNL4030
try:
    sensor = VCNL4030(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing VCNL4030: {e}")
    import sys
    sys.exit(1)

print("VCNL4030 Proximity & Ambient Light Sensor")
print("=" * 45)

# Display sensor information
print(f"Ambient Light Enabled: {sensor.als_enabled}")
print(f"White Channel Enabled: {sensor.white_channel_enabled}")
print(f"Proximity Enabled: {sensor.proximity_enabled}")
print()

# Main reading loop
while True:
    try:
        proximity = sensor.proximity
        lux = sensor.lux
        als = sensor.als
        white = sensor.white

        print(f"Proximity: {proximity}")
        print(f"Ambient Light: {lux:.2f} lux ({als} counts)")
        print(f"White Channel: {white}")

        if sensor.proximity_close_flag:
            print("Object close")
        if sensor.proximity_away_flag:
            print("Object away")

        print("-" * 30)

    except Exception as e:
        print(f"Error reading sensor data: {e}")
        print("-" * 30)

    time.sleep(1)
