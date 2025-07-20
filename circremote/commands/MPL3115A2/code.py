# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_mpl3115a2

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize MPL3115A2
try:
    mpl = adafruit_mpl3115a2.MPL3115A2(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing MPL3115A2: {e}")
    import sys
    sys.exit(1)

print("MPL3115A2 Pressure Sensor")
print("=" * 25)

# Set sea level pressure for altitude calculation
mpl.sea_level_pressure = 1013.25

# Main reading loop
while True:
        # Read sensor values
        pressure = mpl.pressure
        altitude = mpl.altitude
        temperature = mpl.temperature
        
        # Display readings
        print(f"Pressure: {pressure:.1f} Pa")
        print(f"Altitude: {altitude:.1f} m")
        print(f"Temperature: {temperature:.1f}°C")
        print("-" * 30)
        
        time.sleep(30) 