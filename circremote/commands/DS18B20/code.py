# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

import time
import board

from adafruit_onewire.bus import OneWireBus
from adafruit_ds18x20 import DS18X20
from digitalio import DigitalInOut, Direction, Pull


onewire = OneWireBus({{ onewire_pin }})

print("Scanning onewire bus")
devices = onewire.scan()
if len(devices) == 0:
    print("No OneWire devices found")
    exit

if len(devices) > 1:
    print(f"Too many OneWire devices found: {len(devices)}")
    exit

print(f"OneWire device found {devices[0].rom.hex}")

try:
    ds18b20 = DS18X20(onewire, devices[0])
except Exception as e:
    print(f"Error initializing DS18B20: {e}")
    import sys
    sys.exit(1)

print("DS18B20 Temperature Sensor")
print("=" * 35)

# Main reading loop
while True:
    print(f"Temperature: {ds18b20.temperature:.2f}°C")
    time.sleep(10)
