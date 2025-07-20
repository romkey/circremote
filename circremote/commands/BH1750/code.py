# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_bh1750

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize BH1750
try:
    bh1750 = adafruit_bh1750.BH1750(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing BH1750: {e}")
    import sys
    sys.exit(1)

print("BH1750 Light Sensor")
print("=" * 25)

# Display sensor information
print(f"Mode: {bh1750.mode}")
print(f"Resolution: {bh1750.resolution} lux")
print(f"Measurement Time: {bh1750.measurement_time} ms")
print()

# Main reading loop
while True:
    lux = bh1750.lux
    
    print(f"Lux: {lux:.1f} lux")
    
    # Determine light level
    if lux < 1:
        light_level = "Very Dark"
    elif lux < 10:
        light_level = "Dark"
    elif lux < 50:
        light_level = "Low Light"
    elif lux < 200:
        light_level = "Indoor"
    elif lux < 1000:
        light_level = "Bright Indoor"
    elif lux < 10000:
        light_level = "Outdoor"
    else:
        light_level = "Bright Sunlight"
        
    print(f"Light Level: {light_level}")
    print("-" * 30)
    
    time.sleep(30)
