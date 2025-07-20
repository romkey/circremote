# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_ltr390

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize LTR390
try:
    ltr = adafruit_ltr390.LTR390(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing LTR390: {e}")
    import sys
    sys.exit(1)

print("LTR390 UV Light Sensor")
print("=" * 30)

# Display sensor information
print(f"Mode: {ltr.mode}")
print(f"Resolution: {ltr.resolution}")
print(f"Gain: {ltr.gain}")
print(f"Threshold: {ltr.threshold}")
print(f"Interrupt: {ltr.interrupt}")
print()

# Main reading loop
while True:
    uv_raw = ltr.uvs
    uv_index = ltr.uvi
    light = ltr.light
    lux = ltr.lux
    
    print(f"UV Raw: {uv_raw}")
    print(f"UV Index: {uv_index:.2f}")
    print(f"Light: {light}")
    print(f"Lux: {lux:.1f} lux")
    
    # Determine UV level
    if uv_index < 3:
        uv_level = "Low"
    elif uv_index < 6:
        uv_level = "Moderate"
    elif uv_index < 8:
        uv_level = "High"
    elif uv_index < 11:
        uv_level = "Very High"
    else:
        uv_level = "Extreme"
        
    print(f"UV Level: {uv_level}")
    print("-" * 30)
    
    time.sleep(30)
