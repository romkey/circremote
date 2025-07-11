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
        
    except Exception as e:
        print(f"Error reading sensor: {e}")
        time.sleep(5)
