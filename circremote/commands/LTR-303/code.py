# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_ltr329_ltr303

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

try:
    ltr = adafruit_ltr329_ltr303.LTR303(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing LTR-303: {e}")
    import sys
    sys.exit(1)

print("LTR-303 Ambient Light Sensor")
print("=" * 30)

while True:
        # Read sensor values
        visible = ltr.visible_plus_ir_light
        ir = ltr.ir_light
        
        print(f"IR Light: {ir:.1f} lux")
        print(f"Total Light: {visible:.1f} lux")
        print("-" * 30)
        
        time.sleep(10) 
