# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_bmp3xx

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize BMP390
try:
    bmp390 = adafruit_bmp3xx.BMP390(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing BMP390: {e}")
    import sys
    sys.exit(1)

# Configure BMP390
bmp390.sea_level_pressure = 1013.25  # Set sea level pressure in hPa
bmp390.pressure_oversampling = 8
bmp390.temperature_oversampling = 2

print("BMP390 Pressure Sensor")
print("=" * 30)

# Display sensor information
print(f"Pressure Oversampling: {bmp390.pressure_oversampling}")
print(f"Temperature Oversampling: {bmp390.temperature_oversampling}")
print(f"Sea Level Pressure: {bmp390.sea_level_pressure} hPa")
print()

while True:
    temp = bmp390.temperature
    pressure = bmp390.pressure
    altitude = bmp390.altitude
    print(f"Temperature: {temp:.1f}°C")
    print(f"Pressure: {pressure:.1f} hPa")
    print(f"Altitude: {altitude:.1f} m")

    time.sleep(30)
