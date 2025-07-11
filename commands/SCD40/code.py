# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import busio
import adafruit_scd4x

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize SCD40
try:
    scd4x = adafruit_scd4x.SCD4X(i2c)
except Exception as e:
    print(f"Error initializing SCD40: {e}")
    import sys
    sys.exit(1)

print("SCD40 CO2 Sensor")
print("=" * 25)

# Display sensor information
print(f"Serial Number: {scd4x.serial_number}")
print(f"Temperature Offset: {scd4x.temperature_offset}°C")
print(f"Altitude: {scd4x.altitude} m")
print(f"Automatic Self-Calibration: {scd4x.self_calibration_enabled}")
print()

# Start periodic measurements
scd4x.start_periodic_measurement()
print("Started periodic measurements...")
print()

# Main reading loop
while True:
    # Wait for data to be ready
    time.sleep(1)
    
    if scd4x.data_ready:
        try:
            # Read sensor data
            co2 = scd4x.CO2
            temperature = scd4x.temperature
            humidity = scd4x.relative_humidity
            
            # Display readings
            print(f"CO2: {co2} ppm")
            print(f"Temperature: {temperature:.1f}°C")
            print(f"Humidity: {humidity:.1f}%")
            print("-" * 25)
            
        except Exception as e:
            print(f"Error reading sensor data: {e}")
            print("-" * 25)
    else:
        print("Waiting for data...")
        print("-" * 25)
