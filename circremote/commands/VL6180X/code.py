# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_vl6180x

print("VL6180X Time-of-Flight Distance Sensor")
print("=" * 40)

# Initialize I2C bus
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize VL6180X sensor
try:
    vl6180x = adafruit_vl6180x.VL6180X(i2c, address={{ address }})
    print("✓ VL6180X sensor initialized successfully")
    
    # Print sensor information
    print(f"Range: {vl6180x.range} mm")
    print(f"Ambient Light: {vl6180x.ambient_lux} lux")
    
except Exception as e:
    print(f"✗ Error initializing VL6180X: {e}")
    import sys
    sys.exit(1)

print("\nStarting distance and ambient light measurements...")
print("Readings:")

# Main measurement loop
try:
    while True:
        # Read distance and ambient light
        distance = vl6180x.range
        ambient_light = vl6180x.ambient_lux
        
        print(f"Distance: {distance} mm")
        print(f"Ambient Light: {ambient_light:.2f} lux")
        print("-" * 30)
        
        time.sleep(30)  # Wait 30 seconds between readings
        
except KeyboardInterrupt:
    print("\nMeasurement stopped by user")
except Exception as e:
    print(f"\nError during measurement: {e}")

print("***END***") 
