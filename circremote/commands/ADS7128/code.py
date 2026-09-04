# SPDX-FileCopyrightText: 2026 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
from adafruit_ads7128.ads7128 import ADS7128
from adafruit_ads7128.analog_in import AnalogIn

REFERENCE_VOLTAGE = {{ reference_voltage }}

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize ADS7128
try:
    adc = ADS7128(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing ADS7128: {e}")
    import sys
    sys.exit(1)

print("ADS7128 8-Channel 12-Bit ADC")
print("=" * 40)
print(f"Reference Voltage: {REFERENCE_VOLTAGE} V")
print(f"Oversampling: {adc.oversampling}")
print()

# All eight pins default to analog inputs after reset
channels = [AnalogIn(adc, channel) for channel in range(8)]

# Main reading loop
while True:
    try:
        for number, channel in enumerate(channels):
            value = channel.value
            voltage = channel.voltage(REFERENCE_VOLTAGE)
            print(f"Channel {number}: {value:5d}  {voltage:.3f} V")

        print("-" * 30)

    except Exception as e:
        print(f"Error reading ADC: {e}")
        print("-" * 30)

    time.sleep(1)
