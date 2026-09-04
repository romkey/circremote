# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_sgp40

print("SGP40 VOC Sensor")
print("=" * 40)

# Initialize I2C bus
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize SGP40 sensor
try:
    sgp40 = adafruit_sgp40.SGP40(i2c)
except Exception as e:
    print(f"Error initializing SGP40: {e}")
    import sys
    sys.exit(1)

# Display sensor information
try:
    serial = sgp40._serial_number
    print(f"Serial Number: {serial}")
except Exception:
    pass

print("\nStarting VOC measurements...")
print("Note: VOC Index algorithm needs ~1Hz sampling; index readings")
print("stabilize after the first minute of operation.")
print("Readings:")

while True:
    # Raw measurement, uncompensated (assumes 25C / 50% RH)
    raw_uncompensated = sgp40.raw

    # Raw measurement with default compensation values made explicit
    raw_compensated = sgp40.measure_raw(temperature=25, relative_humidity=50)

    # Processed VOC index (0-500, 100 = typical baseline)
    voc_index = sgp40.measure_index(temperature=25, relative_humidity=50)

    print(f"Raw Gas (uncompensated): {raw_uncompensated} (0x{raw_uncompensated:04X})")
    print(f"Raw Gas (compensated 25C/50%RH): {raw_compensated} (0x{raw_compensated:04X})")
    print(f"VOC Index: {voc_index}")

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

    # measure_index requires ~1 second sample spacing for the
    # VOC algorithm to work correctly
    time.sleep(1)
