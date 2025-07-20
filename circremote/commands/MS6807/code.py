# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_ms8607

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize MS6807
try:
    ms6807 = adafruit_ms8607.MS8607(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing MS6807: {e}")
    import sys
    sys.exit(1)

print("MS6807 Pressure Sensor")
print("=" * 25)

# Main reading loop
while True:
        # Read sensor values
        pressure = ms6807.pressure
        temperature = ms6807.temperature
        humidity = ms6807.relative_humidity
        
        # Display readings
        print(f"Pressure: {pressure:.1f} hPa")
        print(f"Temperature: {temperature:.1f}°C")
        print(f"Humidity: {humidity:.1f}%")
        print("-" * 30)
        
        time.sleep(30) 