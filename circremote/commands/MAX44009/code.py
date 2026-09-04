# SPDX-FileCopyrightText: 2026 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
from adafruit_max44009 import MAX44009, IntegrationTime, Mode

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize MAX44009
try:
    sensor = MAX44009(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing MAX44009: {e}")
    import sys
    sys.exit(1)

print("MAX44009 Ambient Light Sensor")
print("=" * 40)

MODE_NAMES = {
    Mode.DEFAULT: "Default (auto, 800ms cycle)",
    Mode.CONTINUOUS: "Continuous (auto, fast updates)",
    Mode.MANUAL: "Manual (800ms cycle)",
    Mode.MANUAL_CONTINUOUS: "Manual Continuous (fast)",
}

INTEGRATION_TIME_NAMES = {
    IntegrationTime.MS_800: "800ms",
    IntegrationTime.MS_400: "400ms",
    IntegrationTime.MS_200: "200ms",
    IntegrationTime.MS_100: "100ms",
    IntegrationTime.MS_50: "50ms",
    IntegrationTime.MS_25: "25ms",
    IntegrationTime.MS_12_5: "12.5ms",
    IntegrationTime.MS_6_25: "6.25ms",
}

# Use continuous mode so readings update faster than the 800ms default cycle
sensor.mode = Mode.CONTINUOUS

# Display sensor information
print(f"Mode: {MODE_NAMES.get(sensor.mode, 'Unknown')}")
print(f"Integration Time: {INTEGRATION_TIME_NAMES.get(sensor.integration_time, 'Unknown')}")
print(f"Current Division Ratio: {'1/8 (extended range)' if sensor.current_division_ratio else 'Full (normal)'}")
print()

time.sleep(0.2)

# Main reading loop
while True:
    try:
        if sensor.overrange:
            print("Lux: OVERRANGE")
        else:
            print(f"Lux: {sensor.lux:.3f}")

        if sensor.interrupt_status:
            print("Interrupt triggered")

        print("-" * 30)

    except Exception as e:
        print(f"Error reading sensor data: {e}")
        print("-" * 30)

    time.sleep(1)
