# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_as7341

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize AS7341
try:
    as7341 = adafruit_as7341.AS7341(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing AS7341: {e}")
    import sys
    sys.exit(1)

print("AS7341 Color & Spectral Sensor")
print("=" * 35)

# Display sensor information
print(f"Integration Time: {as7341.integration_time} ms")
print(f"Gain: {as7341.gain}")
print(f"LED Current: {as7341.led_current} mA")
print(f"LED Enabled: {as7341.led}")
print()

# Main reading loop
while True:
    # Read color data
    red = as7341.channel_415nm + as7341.channel_445nm + as7341.channel_480nm
    green = as7341.channel_515nm + as7341.channel_555nm + as7341.channel_590nm
    blue = as7341.channel_630nm + as7341.channel_680nm
        
    print(f"Color: R={red}, G={green}, B={blue}")
        
    # Calculate color temperature approximation
    if red > 0 and blue > 0:
        ratio = red / blue
        if ratio > 2:
            temp_desc = "Warm"
        elif ratio > 1:
            temp_desc = "Neutral"
        else:
            temp_desc = "Cool"
    else:
        temp_desc = "Unknown"
            
    print(f"Color Temperature: {temp_desc}")
    print("-" * 30)
        
    time.sleep(30)
