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

# Initialize SHT31D
try:
    sht31d = adafruit_sht31d.SHT31D(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing SHT31D: {e}")
    import sys
    sys.exit(1)

print("SHT31-D Temperature & Humidity Sensor")
print("=" * 40)

# Display sensor information
print(f"Heater: {sht31d.heater}")
print(f"Status: {sht31d.status}")
print(f"Reset Status: {sht31d.reset_status}")
print(f"Alert Status: {sht31d.alert_status}")
print(f"Alert High: {sht31d.alert_high}")
print(f"Alert Low: {sht31d.alert_low}")
print()

# Main reading loop
while True:
    temp = sht31d.temperature
    humidity = sht31d.relative_humidity
    
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
