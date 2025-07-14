# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import digitalio

# Initialize TCRT1000
try:
    sensor = digitalio.DigitalInOut({{ pin }})
    sensor.direction = digitalio.Direction.INPUT
    sensor.pull = digitalio.Pull.UP
except Exception as e:
    print(f"Error initializing TCRT1000: {e}")
    import sys
    sys.exit(1)

print("TCRT1000 Infrared Proximity Sensor")
print("=" * 35)

# Main reading loop
while True:
        # Read sensor value
        detected = sensor.value
        
        # Display reading
        if detected:
            print("Object Detected: NO")
        else:
            print("Object Detected: YES")
        print("-" * 30)
        
        time.sleep(0.5) 