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
    
except Exception as e:
    print(f"✗ Error initializing DPS310: {e}")
    import sys
    sys.exit(1)

print("\nStarting pressure and temperature measurements...")
print("Readings:")

while True:
    pressure = dps310.pressure
    temperature = dps310.temperature
        
    altitude = 44330 * (1.0 - (pressure / 101325.0) ** 0.1903)

    print(f"Pressure: {pressure:.2f} hPa")
    print(f"Temperature: {temperature:.2f} °C")
    print(f"Altitude: {altitude:.2f} m")
    print("-" * 30)
        
    time.sleep(30)
