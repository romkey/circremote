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
    sgp40 = adafruit_sgp40.Adafruit_SGP40(i2c)
except Exception as e:
    print(f"Error initializing SGP40: {e}")
    import sys
    sys.exit(1)

print("\nStarting VOC measurements...")
print("Readings:")

# Main measurement loop
try:
    while True:
        voc_index = sgp40.measure_index()
        print(f"VOC Index: {voc_index:.1f}")
        print("-" * 30)
        time.sleep(30)
except KeyboardInterrupt:
    print("\nMeasurement stopped by user")
except Exception as e:
    print(f"\nError during measurement: {e}") 
