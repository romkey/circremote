# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_vl53l0x

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize VL53L0X
try:
    vl53 = adafruit_vl53l0x.VL53L0X(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing VL53L0X: {e}")
    import sys
    sys.exit(1)

print("VL53L0X Time-of-Flight Distance Sensor")
print("=" * 45)

# Display sensor information
print(f"Measurement Timing Budget: {vl53.measurement_timing_budget} ms")
print(f"Range: {vl53.range} mm")
print(f"Signal Rate: {vl53.signal_rate} MCPS")
print(f"Ambient Rate: {vl53.ambient_rate} MCPS")
print(f"Spad Count: {vl53.spad_count}")
print()

# Main reading loop
while True:
    distance = vl53.range
    signal_rate = vl53.signal_rate
    ambient_rate = vl53.ambient_rate
    spad_count = vl53.spad_count
    
    print(f"Distance: {distance} mm")
    print(f"Signal Rate: {signal_rate:.2f} MCPS")
    print(f"Ambient Rate: {ambient_rate:.2f} MCPS")
    print(f"SPAD Count: {spad_count}")
    
    # Determine distance level
    if distance < 50:
        distance_level = "Very Close"
    elif distance < 100:
        distance_level = "Close"
    elif distance < 500:
        distance_level = "Medium"
    elif distance < 1000:
        distance_level = "Far"
    else:
        distance_level = "Very Far"
        
    print(f"Distance Level: {distance_level}")
    print("-" * 30)
    
    time.sleep(30)
