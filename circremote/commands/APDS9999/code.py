# SPDX-FileCopyrightText: 2026 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
from adafruit_apds9999 import (
    APDS9999,
    LedCurrent,
    LightGain,
    LightResolution,
    ProximityResolution,
)

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize APDS9999
try:
    sensor = APDS9999(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing APDS9999: {e}")
    import sys
    sys.exit(1)

print("APDS9999 RGB, IR & Proximity Sensor")
print("=" * 40)

# Enable the light and proximity engines, and RGB (rather than ALS-only) mode
sensor.light_sensor_enabled = True
sensor.proximity_sensor_enabled = True
sensor.rgb_mode = True

# Display sensor information
try:
    print(f"Light Gain: {LightGain.get_name(sensor.light_gain)}")
    print(f"Light Resolution: {LightResolution.get_name(sensor.light_resolution)}")
    print(f"Proximity Resolution: {ProximityResolution.get_name(sensor.proximity_resolution)}")
    print(f"LED Current: {LedCurrent.get_name(sensor.led_current)}")
except Exception:
    pass
print()

# Main reading loop
while True:
    time.sleep(1)

    try:
        r, g, b, ir = sensor.rgb_ir
        proximity = sensor.proximity
        lux = sensor.calculate_lux(g)

        print(f"Red: {r}")
        print(f"Green: {g}")
        print(f"Blue: {b}")
        print(f"IR: {ir}")
        print(f"Lux: {lux:.2f}")
        print(f"Proximity: {proximity}")

        if sensor.proximity_read_overflow:
            print("Proximity reading overflowed")

        print("-" * 30)

    except Exception as e:
        print(f"Error reading sensor data: {e}")
        print("-" * 30)
