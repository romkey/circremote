# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_sht4x

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize SHT41 sensor
try:
    sht41 = adafruit_sht4x.SHT4x(i2c, address={{ address }})
    print("✓ SHT41 sensor initialized successfully")
    
    # Configure sensor settings
    sht41.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION
    print(f"Mode: {sht41.mode}")
    
except Exception as e:
    print(f"✗ Error initializing SHT41: {e}")
    import sys
    sys.exit(1)

print("SHT41 Temperature and Humidity Sensor")
print("=" * 40)

print("\nStarting temperature and humidity measurements...")
print("Readings:")

# Main measurement loop
try:
    while True:
        # Read temperature and humidity
        temperature, relative_humidity = sht41.measurements
        
        # Calculate absolute humidity (approximate)
        # Using simplified formula
        absolute_humidity = (6.112 * 2.71828**((17.67 * temperature) / (temperature + 243.5)) * relative_humidity * 2.1674) / (273.15 + temperature)
        
        print(f"Temperature: {temperature:.2f} °C")
        print(f"Relative Humidity: {relative_humidity:.2f} %")
        print(f"Absolute Humidity: {absolute_humidity:.2f} g/m³")
        print("-" * 30)
        
        time.sleep(30)  # Wait 30 seconds between readings
        
except KeyboardInterrupt:
    print("\nMeasurement stopped by user")
except Exception as e:
    print(f"\nError during measurement: {e}") 
