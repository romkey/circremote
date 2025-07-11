# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_mmc56x3

print("MMC5603 3-Axis Magnetometer")
print("=" * 40)

# Initialize I2C bus
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize MMC5603 sensor
try:
    mmc5603 = adafruit_mmc56x3.MMC5603(i2c, address={{ address }})
    print("✓ MMC5603 sensor initialized successfully")
    
    # Configure sensor settings
    mmc5603.magnetic_field_range = adafruit_mmc56x3.MagneticFieldRange.RANGE_30_GAUSS
    mmc5603.data_rate = adafruit_mmc56x3.DataRate.RATE_100_HZ
    
    print(f"Magnetic Field Range: {mmc5603.magnetic_field_range}")
    print(f"Data Rate: {mmc5603.data_rate}")
    
except Exception as e:
    print(f"✗ Error initializing MMC5603: {e}")
    import sys
    sys.exit(1)

print("\nStarting magnetic field measurements...")
print("Magnetic field readings (Gauss):")

# Main measurement loop
try:
    while True:
        # Read magnetic field values
        mag_x, mag_y, mag_z = mmc5603.magnetic
        
        # Calculate magnitude
        magnitude = (mag_x**2 + mag_y**2 + mag_z**2)**0.5
        
        print(f"X: {mag_x:.3f} Gauss")
        print(f"Y: {mag_y:.3f} Gauss")
        print(f"Z: {mag_z:.3f} Gauss")
        print(f"Magnitude: {magnitude:.3f} Gauss")
        print("-" * 30)
        
        time.sleep(30)  # Wait 30 seconds between readings
        
except KeyboardInterrupt:
    print("\nMeasurement stopped by user")
except Exception as e:
    print(f"\nError during measurement: {e}") 
