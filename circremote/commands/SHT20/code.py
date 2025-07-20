# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_sht31d

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize SHT20
try:
    sht20 = adafruit_sht31d.SHT31D(i2c, address={{ address }}, address=0x40)  # SHT20 uses address 0x40
except Exception as e:
    print(f"Error initializing SHT20: {e}")
    import sys
    sys.exit(1)

print("SHT20 Temperature & Humidity Sensor")
print("=" * 40)

# Display sensor information
print(f"I2C Address: 0x40")
print(f"Heater: {sht20.heater}")
print(f"Status: {sht20.status}")
print(f"Reset Status: {sht20.reset_status}")
print()

# Main reading loop
while True:
    temp = sht20.temperature
    humidity = sht20.relative_humidity
    
    print(f"Temperature: {temp:.1f}°C")
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
