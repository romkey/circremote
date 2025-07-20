# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_vl53l4cd

print("VL53L4CX Time-of-Flight Distance Sensor")
print("=" * 40)

# Initialize I2C bus
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize VL53L4CX sensor
try:
    vl53l4cx = adafruit_vl53l4cd.VL53L4CD(i2c, address={{ address }})
    print("✓ VL53L4CX sensor initialized successfully")
    
    # Configure sensor settings
    vl53l4cx.inter_measurement = 0
    vl53l4cx.timing_budget = 200
    vl53l4cx.start_ranging()
    
    print(f"Timing Budget: {vl53l4cx.timing_budget}ms")
    print(f"Inter-Measurement: {vl53l4cx.inter_measurement}ms")
    
except Exception as e:
    print(f"✗ Error initializing VL53L4CX: {e}")
    import sys
    sys.exit(1)

print("\nStarting distance measurements...")
print("Distance readings (mm):")

# Main measurement loop
try:
    while True:
        # Read distance
        if vl53l4cx.data_ready:
            distance = vl53l4cx.distance
            ambient = vl53l4cx.ambient
            status = vl53l4cx.status
            
            print(f"Distance: {distance} mm")
            print(f"Ambient: {ambient}")
            print(f"Status: {status}")
        else:
            print("No data available")
        
        print("-" * 30)
        time.sleep(30)  # Wait 30 seconds between readings
        
except KeyboardInterrupt:
    print("\nMeasurement stopped by user")
    vl53l4cx.stop_ranging()
except Exception as e:
    print(f"\nError during measurement: {e}") 
