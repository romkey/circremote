# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_adxl34x

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize ADXL343
try:
    adxl = adafruit_adxl34x.ADXL343(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing ADXL343: {e}")
    import sys
    sys.exit(1)

print("ADXL343 3-Axis Accelerometer")
print("=" * 30)

# Display sensor information
print(f"Range: ±{adxl.range}g")
print(f"Data Rate: {adxl.data_rate} Hz")
print()

# Main reading loop
while True:
        # Read accelerometer values
        x, y, z = adxl.acceleration
        
        # Display readings
        print(f"X: {x:.2f} m/s²")
        print(f"Y: {y:.2f} m/s²")
        print(f"Z: {z:.2f} m/s²")
        print("-" * 30)
        
        time.sleep(1) 