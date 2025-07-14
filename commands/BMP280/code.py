# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_bmp280

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize BMP280
try:
    bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing BMP280: {e}")
    import sys
    sys.exit(1)

print("BMP280 Pressure Sensor")
print("=" * 25)

# Set sea level pressure for altitude calculation
bmp280.sea_level_pressure = 1013.25

# Main reading loop
while True:
        # Read sensor values
        pressure = bmp280.pressure
        temperature = bmp280.temperature
        altitude = bmp280.altitude
        
        # Display readings
        print(f"Pressure: {pressure:.1f} hPa")
        print(f"Temperature: {temperature:.1f}°C")
        print(f"Altitude: {altitude:.1f} m")
        print("-" * 30)
        
        time.sleep(30) 