# SPDX-FileCopyrightText: 2026 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_gp8403

OUTPUT_RANGE = {{ output_range }}
VOLTAGE_0 = {{ voltage0 }}
VOLTAGE_1 = {{ voltage1 }}

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

if OUTPUT_RANGE == 5:
    output_range = adafruit_gp8403.Range.RANGE_5V
    full_scale = 5.0
else:
    output_range = adafruit_gp8403.Range.RANGE_10V
    full_scale = 10.0

# Initialize GP8403
try:
    dac = adafruit_gp8403.GP8403(i2c, address={{ address }}, output_range=output_range)
except Exception as e:
    print(f"Error initializing GP8403: {e}")
    import sys
    sys.exit(1)

print("GP8403 2-Channel I2C DAC")
print("=" * 30)
print(f"Output Range: 0-{full_scale:.0f}V")
print()

# Clamp requested voltages to the selected output range
voltage_0 = min(max(VOLTAGE_0, 0.0), full_scale)
voltage_1 = min(max(VOLTAGE_1, 0.0), full_scale)

if voltage_0 != VOLTAGE_0 or voltage_1 != VOLTAGE_1:
    print("Requested voltage outside output range - clamped")

try:
    dac.channel_0.voltage = voltage_0
    dac.channel_1.voltage = voltage_1
except Exception as e:
    print(f"Error setting output voltages: {e}")
    import sys
    sys.exit(1)

print(f"Set Channel 0: {voltage_0:.2f}V")
print(f"Set Channel 1: {voltage_1:.2f}V")
print()
print("Outputs are held until the board is reset.")
print("Note: values are not written to NVM, so they are lost at power off.")
print()

# Main loop - report the current output settings
while True:
    try:
        voltages = dac.voltages
        raw_values = dac.raw_values

        print(f"Channel 0: {voltages[0]:.2f}V (raw {raw_values[0]})")
        print(f"Channel 1: {voltages[1]:.2f}V (raw {raw_values[1]})")
        print("-" * 30)

    except Exception as e:
        print(f"Error reading DAC: {e}")
        print("-" * 30)

    time.sleep(10)
