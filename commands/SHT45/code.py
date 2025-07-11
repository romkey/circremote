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

# Initialize SHT45 sensor
try:
    sht45 = adafruit_sht4x.SHT4x(i2c, address={{ address }})
    print("✓ SHT45 sensor initialized successfully")
    
    # Configure sensor settings
    sht45.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION
    print(f"Mode: {sht45.mode}")
    
except Exception as e:
    print(f"✗ Error initializing SHT45: {e}")
    import sys
    sys.exit(1)

print("SHT45 Temperature and Humidity Sensor")
print("=" * 40)

print("\nStarting temperature and humidity measurements...")
print("Readings:")

# Main measurement loop
try:
    while True:
        # Read temperature and humidity
        temperature, relative_humidity = sht45.measurements
        
        # Calculate heat index (approximate)
        if temperature >= 26.7:
            hi = -8.78469475556 + 1.61139411 * temperature + 2.33854883889 * relative_humidity - 0.14611605 * temperature * relative_humidity - 0.012308094 * temperature**2 - 0.0164248277778 * relative_humidity**2 + 0.002211732 * temperature**2 * relative_humidity + 0.00072546 * temperature * relative_humidity**2 - 0.000003582 * temperature**2 * relative_humidity**2
        else:
            hi = temperature
        
        print(f"Temperature: {temperature:.2f} °C")
        print(f"Relative Humidity: {relative_humidity:.2f} %")
        print(f"Heat Index: {hi:.2f} °C")
        print("-" * 30)
        
        time.sleep(30)  # Wait 30 seconds between readings
        
except KeyboardInterrupt:
    print("\nMeasurement stopped by user")
except Exception as e:
    print(f"\nError during measurement: {e}") 
