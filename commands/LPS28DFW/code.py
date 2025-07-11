# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_lps2x

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize LPS28DFW
try:
    lps = adafruit_lps2x.LPS28(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing LPS28DFW: {e}")
    import sys
    sys.exit(1)

print("LPS28DFW Pressure Sensor")
print("=" * 25)

# Main reading loop
while True:
    try:
        # Read sensor values
        pressure = lps.pressure
        temperature = lps.temperature
        
        # Display readings
        print(f"Pressure: {pressure:.1f} hPa")
        print(f"Temperature: {temperature:.1f}°C")
        print("-" * 30)
        
        time.sleep(30)
        
    except Exception as e:
        print(f"Error reading sensor: {e}")
        time.sleep(5) 