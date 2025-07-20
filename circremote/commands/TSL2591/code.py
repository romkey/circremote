# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_tsl2591

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize TSL2591
try:
    tsl = adafruit_tsl2591.TSL2591(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing TSL2591: {e}")
    import sys
    sys.exit(1)

print("TSL2591 Light Sensor")
print("=" * 30)

# Display sensor information
print(f"Gain: {tsl.gain}")
print(f"Integration Time: {tsl.integration_time}")
print(f"Lux Range: {tsl.lux_range}")
print()

# Main reading loop
while True:
    lux = tsl.lux
    infrared = tsl.infrared
    visible = tsl.visible
    full_spectrum = tsl.full_spectrum
    
    print(f"Lux: {lux:.1f} lux")
    print(f"Infrared: {infrared}")
    print(f"Visible: {visible}")
    print(f"Full Spectrum: {full_spectrum}")
    
    # Determine light level
    if lux < 10:
        light_level = "Dark"
    elif lux < 50:
        light_level = "Low Light"
    elif lux < 200:
        light_level = "Indoor"
    elif lux < 1000:
        light_level = "Bright Indoor"
    else:
        light_level = "Outdoor"
        
    print(f"Light Level: {light_level}")
    print("-" * 30)
    
    time.sleep(30)
