# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_dps310

print("DPS310 Barometric Pressure Sensor")
print("=" * 40)

# Initialize I2C bus
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize DPS310 sensor
try:
    dps310 = adafruit_dps310.DPS310(i2c, address={{ address }})
    print("✓ DPS310 sensor initialized successfully")
    
    # Configure sensor settings
    dps310.pressure_oversample_count = adafruit_dps310.SampleCount.COUNT_64
    dps310.temperature_oversample_count = adafruit_dps310.SampleCount.COUNT_64
    dps310.pressure_rate = adafruit_dps310.Rate.RATE_1_HZ
    dps310.temperature_rate = adafruit_dps310.Rate.RATE_1_HZ
    
    print(f"Pressure Oversample Count: {dps310.pressure_oversample_count}")
    print(f"Temperature Oversample Count: {dps310.temperature_oversample_count}")
    print(f"Pressure Rate: {dps310.pressure_rate}")
    print(f"Temperature Rate: {dps310.temperature_rate}")
    
except Exception as e:
    print(f"✗ Error initializing DPS310: {e}")
    import sys
    sys.exit(1)

print("\nStarting pressure and temperature measurements...")
print("Readings:")

# Main measurement loop
try:
    while True:
        # Read pressure and temperature
        pressure = dps310.pressure
        temperature = dps310.temperature
        
        # Calculate altitude (approximate)
        altitude = 44330 * (1.0 - (pressure / 101325.0) ** 0.1903)
        
        print(f"Pressure: {pressure:.2f} hPa")
        print(f"Temperature: {temperature:.2f} °C")
        print(f"Altitude: {altitude:.2f} m")
        print("-" * 30)
        
        time.sleep(30)  # Wait 30 seconds between readings
        
except KeyboardInterrupt:
    print("\nMeasurement stopped by user")
except Exception as e:
    print(f"\nError during measurement: {e}") 
