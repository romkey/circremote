# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_tlv493d

print("TLV493D 3-Axis Magnetometer")
print("=" * 40)

# Initialize I2C bus
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize TLV493D sensor
try:
    tlv493d = adafruit_tlv493d.TLV493D(i2c)
    print("✓ TLV493D sensor initialized successfully")
    
except Exception as e:
    print(f"✗ Error initializing TLV493D: {e}")
    import sys
    sys.exit(1)

print("\nStarting magnetic field measurements...")
print("Magnetic field readings (μT):")

# Main measurement loop
try:
    while True:
        # Read magnetic field values
        mag_x, mag_y, mag_z = tlv493d.magnetic
        
        # Calculate magnitude
        magnitude = (mag_x**2 + mag_y**2 + mag_z**2)**0.5
        
        print(f"X: {mag_x:.2f} μT")
        print(f"Y: {mag_y:.2f} μT")
        print(f"Z: {mag_z:.2f} μT")
        print(f"Magnitude: {magnitude:.2f} μT")
        print("-" * 30)
        
        time.sleep(10)
        
except KeyboardInterrupt:
    print("\nMeasurement stopped by user")
except Exception as e:
    print(f"\nError during measurement: {e}") 
