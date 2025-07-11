# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_vl53l1x

print("VL53L1X Time-of-Flight Distance Sensor")
print("=" * 40)

# Initialize I2C bus
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize VL53L1X sensor
try:
    vl53l1x = adafruit_vl53l1x.VL53L1X(i2c, address={{ address }})
    print("✓ VL53L1X sensor initialized successfully")
    
    # Print sensor information
    print(f"Distance Mode: {vl53l1x.distance_mode}")
    print(f"Timing Budget: {vl53l1x.timing_budget}ms")
    print(f"Inter-Measurement Period: {vl53l1x.inter_measurement}ms")
    
except Exception as e:
    print(f"✗ Error initializing VL53L1X: {e}")
    import sys
    sys.exit(1)

print("\nStarting distance measurements...")
print("Distance readings (mm):")

# Main measurement loop
try:
    while True:
        # Read distance
        distance = vl53l1x.distance
        
        if distance is not None:
            print(f"Distance: {distance} mm")
        else:
            print("Distance: No reading")
        
        time.sleep(30)  # Wait 30 seconds between readings
        
except KeyboardInterrupt:
    print("\nMeasurement stopped by user")
except Exception as e:
    print(f"\nError during measurement: {e}")

print("***END***") 
