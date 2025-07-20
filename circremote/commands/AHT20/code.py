# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_ahtx0

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize AHT20
try:
    aht20 = adafruit_ahtx0.AHTx0(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing AHT20: {e}")
    import sys
    sys.exit(1)

print("AHT20 Temperature & Humidity Sensor")
print("=" * 40)

# Display sensor information
print(f"Temperature Resolution: 0.01°C")
print(f"Humidity Resolution: 0.024%")
print(f"Operating Range: -40°C to +85°C")
print(f"Humidity Range: 0-100%")
print()

# Main reading loop
while True:
    temp = aht20.temperature
    humidity = aht20.relative_humidity
    
    print(f"Temperature: {temp:.1f}°C")
    print(f"Humidity: {humidity:.1f}%")
    print("-" * 30)
    
    time.sleep(30)
    print(f"Temperature: {temp:.2f}°C")
    print(f"Humidity: {humidity:.2f}%")
    
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
