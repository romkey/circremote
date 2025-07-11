# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_tmp117

print("TMP117 High-Precision Temperature Sensor")
print("=" * 40)

# Initialize I2C bus
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize TMP117 sensor
try:
    tmp117 = adafruit_tmp117.TMP117(i2c, address={{ address }})
    print("✓ TMP117 sensor initialized successfully")
    
    # Print sensor information
    print(f"Temperature Resolution: {tmp117.temperature_resolution} bits")
    print(f"Conversion Mode: {tmp117.conversion_mode}")
    print(f"Data Ready: {tmp117.data_ready}")
    
except Exception as e:
    print(f"✗ Error initializing TMP117: {e}")
    import sys
    sys.exit(1)

print("\nStarting temperature measurements...")
print("Temperature readings (°C):")

# Main measurement loop
try:
    while True:
        # Read temperature
        temperature = tmp117.temperature
        
        # Convert to Fahrenheit
        fahrenheit = temperature * 9/5 + 32
        
        print(f"Temperature: {temperature:.3f} °C ({fahrenheit:.3f} °F)")
        print("-" * 30)
        
        time.sleep(30)  # Wait 30 seconds between readings
        
except KeyboardInterrupt:
    print("\nMeasurement stopped by user")
except Exception as e:
    print(f"\nError during measurement: {e}") 
