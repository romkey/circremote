# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import adafruit_ds18x20
from digitalio import DigitalInOut, Direction, Pull

# Initialize OneWire bus
try:
    onewire = {{ pin }}
except Exception as e:
    print(f"Error initializing DS18B20: {e}")
    import sys
    sys.exit(1)

# Initialize DS18B20
try:
    ds18b20 = adafruit_ds18x20.DS18X20(onewire)
except Exception as e:
    print(f"Error initializing DS18B20: {e}")
    import sys
    sys.exit(1)

print("DS18B20 Temperature Sensor")
print("=" * 35)

# Scan for devices
roms = ds18b20.scan()
print(f"Found {len(roms)} DS18B20 device(s)")

# Display sensor information
for i, rom in enumerate(roms):
    print(f"Device {i+1}: {[hex(x) for x in rom]}")
    print(f"Temperature Resolution: {ds18b20.resolution} bits")
print()

# Main reading loop
while True:
    # Read temperature from all devices
    for i, rom in enumerate(roms):
        temp = ds18b20.read_temperature(rom)
        print(f"Device {i+1} Temperature: {temp:.2f}°C")
                
    time.sleep(30) 
