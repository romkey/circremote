# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
from adafruit_sgp41.sgp41 import SGP41

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize SGP41
try:
    sgp41 = SGP41(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing SGP41: {e}")
    import sys
    sys.exit(1)

print("SGP41 VOC & NOx Sensor")
print("=" * 30)

# Display sensor information
try:
    serial_number = sgp41.serial_number
    print(f"Serial Number: {serial_number}")
except Exception:
    pass

try:
    print(f"Self Test Passed: {sgp41.self_test_passed}")
except Exception:
    pass
print()

# The NOx signal needs the heater conditioned before the first measurement
print("Conditioning sensor (10 seconds)...")
for i in range(10):
    try:
        sgp41.conditioning()
    except Exception as e:
        print(f"Error during conditioning: {e}")
        break
    time.sleep(1)

print("Sensor ready.")
print()
print("Note: the gas index algorithm needs 1 Hz sampling. Both indices read 0")
print("during the first ~45 seconds of warm-up, then settle in the range 1-500")
print("(VOC baseline 100, NOx baseline 1).")
print("Readings:")
print()

# Main reading loop
while True:
    try:
        raw_voc = sgp41.raw_voc
        raw_nox = sgp41.raw_nox

        # Processed index values, compensated with the library's defaults
        # of 25C / 50%RH unless sgp41.temperature and sgp41.relative_humidity
        # have been set from an external temperature/humidity sensor
        voc_index, nox_index = sgp41.measure_index()

        print(f"Raw VOC: {raw_voc}")
        print(f"Raw NOx: {raw_nox}")
        print(f"VOC Index: {voc_index}")
        print(f"NOx Index: {nox_index}")

        # Interpret the VOC index
        if voc_index == 0:
            quality = "Warming Up / Not Ready"
        elif voc_index < 80:
            quality = "Improving Air Quality"
        elif voc_index <= 120:
            quality = "Typical / Baseline"
        elif voc_index <= 200:
            quality = "Elevated VOCs"
        elif voc_index <= 350:
            quality = "High VOCs"
        else:
            quality = "Very High VOCs"

        print(f"Air Quality: {quality}")
        print("-" * 30)

    except Exception as e:
        print(f"Error reading sensor data: {e}")
        print("-" * 30)

    # The gas index algorithm requires ~1 second sample spacing
    time.sleep(1)
