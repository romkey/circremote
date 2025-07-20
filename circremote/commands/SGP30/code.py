# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_sgp30

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize SGP30 sensor
try:
    sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
    print("✓ SGP30 sensor initialized successfully")
    
    # Print sensor information
    print(f"Serial Number: {sgp30.serial}")
    
except Exception as e:
    print(f"✗ Error initializing SGP30: {e}")
    import sys
    sys.exit(1)

print("SGP30 Air Quality Sensor")
print("=" * 40)

print("\nStarting air quality measurements...")
print("Readings:")

# Main measurement loop
try:
    while True:
        # Read air quality data
        eco2, tvoc = sgp30.iaq_measure()
        
        # Get baseline values
        eco2_baseline, tvoc_baseline = sgp30.baseline_eCO2, sgp30.baseline_TVOC
        
        print(f"eCO2: {eco2} ppm")
        print(f"TVOC: {tvoc} ppb")
        print(f"eCO2 Baseline: {eco2_baseline}")
        print(f"TVOC Baseline: {tvoc_baseline}")
        print("-" * 30)
        
        time.sleep(30)  # Wait 30 seconds between readings
        
except KeyboardInterrupt:
    print("\nMeasurement stopped by user")
except Exception as e:
    print(f"\nError during measurement: {e}") 
