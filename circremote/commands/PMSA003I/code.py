# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
from adafruit_pm25.i2c import PM25_I2C

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize PM2.5 sensor
try:
    pm25 = PM25_I2C(i2c)
except Exception as e:
    print(f"Error initializing PMA003I: {e}")
    import sys
    sys.exit(1)

print("PMA003I Particulate Matter Sensor")
print("=" * 40)

# Display sensor information
print("Sensor Type: PMSA003I")
print("Interface: I2C")
print("Particle Size Range: 0.3 - 10 μm")
print()

# Main reading loop
while True:
        # Read sensor values
        aqdata = pm25.read()
        
        # Display readings
        print("PM1.0 Standard: {} μg/m³".format(aqdata["pm10 standard"]))
        print("PM2.5 Standard: {} μg/m³".format(aqdata["pm25 standard"]))
        print("PM10 Standard: {} μg/m³".format(aqdata["pm100 standard"]))
        print()
        print("PM1.0 Environmental: {} μg/m³".format(aqdata["pm10 env"]))
        print("PM2.5 Environmental: {} μg/m³".format(aqdata["pm25 env"]))
        print("PM10 Environmental: {} μg/m³".format(aqdata["pm100 env"]))
        print()
        print("Particles > 0.3μm: {} / 0.1L".format(aqdata["particles 03um"]))
        print("Particles > 0.5μm: {} / 0.1L".format(aqdata["particles 05um"]))
        print("Particles > 1.0μm: {} / 0.1L".format(aqdata["particles 10um"]))
        print("Particles > 2.5μm: {} / 0.1L".format(aqdata["particles 25um"]))
        print("Particles > 5.0μm: {} / 0.1L".format(aqdata["particles 50um"]))
        print("Particles > 10μm: {} / 0.1L".format(aqdata["particles 100um"]))
        print("-" * 30)
        
        time.sleep(30) 
