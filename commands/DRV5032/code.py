# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import digitalio

# Initialize DRV5032
try:
    sensor = digitalio.DigitalInOut({{ pin }})
    sensor.direction = digitalio.Direction.INPUT
    sensor.pull = digitalio.Pull.UP
except Exception as e:
    print(f"Error initializing DRV5032: {e}")
    import sys
    sys.exit(1)

print("DRV5032 Hall Effect Sensor")
print("=" * 25)

# Main reading loop
while True:
        # Read sensor value
        detected = sensor.value
        
        # Display reading
        if detected:
            print("Magnetic Field: DETECTED")
        else:
            print("Magnetic Field: NOT DETECTED")
        print("-" * 30)
        
        time.sleep(0.5) 