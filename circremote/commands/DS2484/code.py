# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_ds2484

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize DS2484
try:
    ds2484 = adafruit_ds2484.DS2484(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing DS2484: {e}")
    import sys
    sys.exit(1)

print("DS2484 1-Wire Master Controller")
print("=" * 30)

# Main reading loop
while True:
        # Scan for 1-Wire devices
        devices = ds2484.scan()
        
        print(f"Found {len(devices)} 1-Wire device(s):")
        for i, device in enumerate(devices):
            print(f"  Device {i+1}: {device}")
        
        print("-" * 30)
        time.sleep(10) 