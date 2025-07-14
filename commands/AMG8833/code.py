# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_amg88xx

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize AMG8833
try:
    amg = adafruit_amg88xx.AMG88XX(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing AMG8833: {e}")
    import sys
    sys.exit(1)

print("AMG8833 8x8 Thermal Camera")
print("=" * 25)

# Main reading loop
while True:
        # Read sensor values
        pixels = amg.pixels
        
        # Find min and max temperatures
        min_temp = min([min(row) for row in pixels])
        max_temp = max([max(row) for row in pixels])
        
        # Display readings
        print(f"Min Temperature: {min_temp:.1f}°C")
        print(f"Max Temperature: {max_temp:.1f}°C")
        print("8x8 Temperature Grid:")
        
        # Display the 8x8 grid
        for row in pixels:
            print(" ".join([f"{temp:6.1f}" for temp in row]))
        
        print("-" * 30)
        time.sleep(5) 