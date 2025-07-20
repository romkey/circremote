# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_sensirion

print("SEN55 Environmental Sensor")
print("=" * 40)

# Initialize I2C bus
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize SEN55 sensor
try:
    sen55 = adafruit_sensirion.SEN55(i2c)
except Exception as e:
    print(f"Error initializing SEN55: {e}")
    import sys
    sys.exit(1)

# Print sensor information
print(f"Product Type: {sen55.product_type}")
print(f"Serial Number: {sen55.serial_number}")

print("\nStarting environmental measurements...")
print("Readings:")

# Main measurement loop
try:
    while True:
        # Read environmental data
        temperature, humidity, voc_index, nox_index = sen55.measurements
        print(f"Temperature: {temperature:.2f} °C")
        print(f"Relative Humidity: {humidity:.2f} %")
        print(f"VOC Index: {voc_index:.1f}")
        print(f"NOx Index: {nox_index:.1f}")
        print("-" * 30)
        time.sleep(30)  # Wait 30 seconds between readings
except KeyboardInterrupt:
    print("\nMeasurement stopped by user")
except Exception as e:
    print(f"\nError during measurement: {e}") 
