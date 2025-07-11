# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_hdc3020

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize HDC3022
try:
    hdc3022 = adafruit_hdc3020.HDC3020(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing HDC3022: {e}")
    import sys
    sys.exit(1)

    import sys
    sys.exit(1)

print("HDC3022 Temperature & Humidity Sensor")
print("=" * 40)

# Display sensor information
print(f"Serial Number: {hdc3022.serial_number}")
print(f"Manufacturer ID: {hdc3022.manufacturer_id}")
print(f"Device ID: {hdc3022.device_id}")
print(f"Status: {hdc3022.status}")
print()

# Main reading loop
while True:
    try:
        temp = hdc3022.temperature
        humidity = hdc3022.relative_humidity        print(f"Temperature: {temp:.1f}°C")
        print(f"Humidity: {humidity:.1f}%")
        
        # Determine comfort level
        if humidity < 30:
            comfort = "Too Dry"
        elif humidity < 60:
            comfort = "Comfortable"
        else:
            comfort = "Too Humid"
            
        print(f"Comfort Level: {comfort}")
        print("-" * 30)
        
        time.sleep(30)
        
    except Exception as e:
        print(f"Error reading sensor: {e}")
        time.sleep(5)
