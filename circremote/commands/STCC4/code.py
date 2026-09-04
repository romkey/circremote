# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_stcc4

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize STCC4
try:
    stcc4 = adafruit_stcc4.STCC4(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing STCC4: {e}")
    import sys
    sys.exit(1)

print("STCC4 CO2 Sensor")
print("=" * 25)

# Display sensor information
try:
    print(f"Product ID: {stcc4.product_id}")
except Exception:
    pass
try:
    print(f"Status: {stcc4.status}")
except Exception:
    pass
print()

# Start continuous measurements (1 second sampling interval)
stcc4.continuous_measurement = True
print("Started continuous measurements...")
print()

# Main reading loop
while True:
    time.sleep(5)

    try:
        # Read sensor data
        co2 = stcc4.CO2
        temperature = stcc4.temperature
        humidity = stcc4.relative_humidity

        # Display readings
        print(f"CO2: {co2} ppm")
        print(f"Temperature: {temperature:.1f}°C")
        print(f"Humidity: {humidity:.1f}%")
        print("-" * 25)

    except Exception as e:
        print(f"Error reading sensor data: {e}")
        print("-" * 25)
