# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_veml7700

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize VEML7700
try:
    veml7700 = adafruit_veml7700.VEML7700(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing VEML7700: {e}")
    import sys
    sys.exit(1)

print("VEML7700 Ambient Light Sensor")
print("=" * 35)

# Display sensor information
print(f"Integration Time: {veml7700.integration_time}")
print(f"Gain: {veml7700.gain}")
print(f"Power Save Mode: {veml7700.power_save}")
print()

# Main reading loop
while True:
    lux = veml7700.lux
    white = veml7700.white
    als = veml7700.als
    
    print(f"Lux: {lux:.2f} lux")
    print(f"White: {white}")
    print(f"ALS: {als}")
    
    # Determine light level
    if lux < 0.1:
        light_level = "Very Dark"
    elif lux < 1:
        light_level = "Dark"
    elif lux < 10:
        light_level = "Low Light"
    elif lux < 100:
        light_level = "Indoor"
    elif lux < 1000:
        light_level = "Bright Indoor"
    else:
        light_level = "Outdoor"
        
    print(f"Light Level: {light_level}")
    print("-" * 30)
    
    time.sleep(30)
