# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
from adafruit_opt4048 import OPT4048, ConversionTime, Mode, Range

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize OPT4048
try:
    opt = OPT4048(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing OPT4048: {e}")
    import sys
    sys.exit(1)

print("OPT4048 Tristimulus XYZ Color Sensor")
print("=" * 40)

# Configure for continuous auto-ranged measurements
try:
    opt.range = Range.AUTO
    opt.conversion_time = ConversionTime.TIME_100MS
    opt.mode = Mode.CONTINUOUS
except Exception as e:
    print(f"Error configuring sensor: {e}")
    import sys
    sys.exit(1)

# Display sensor configuration
print(f"Range: {Range.get_name(opt.range)}")
print(f"Conversion Time: {ConversionTime.get_name(opt.conversion_time)}")
print(f"Mode: {Mode.get_name(opt.mode)}")
print()

# Main reading loop
while True:
    try:
        # Raw channel counts
        ch0, ch1, ch2, ch3 = opt.all_channels

        # CIE XYZ tristimulus values
        x_tri, y_tri, z_tri = opt.xyz

        # CIE chromaticity coordinates and illuminance
        cie_x, cie_y, lux = opt.cie

        print(f"Channels: X={ch0} Y={ch1} Z={ch2} W={ch3}")
        print(f"Tristimulus: X={x_tri:.4f} Y={y_tri:.4f} Z={z_tri:.4f}")
        print(f"CIE Chromaticity: x={cie_x:.4f} y={cie_y:.4f}")
        print(f"Illuminance: {lux:.2f} lux")

        # Correlated color temperature, only meaningful with light present
        try:
            cct = opt.calculate_color_temperature(cie_x, cie_y)
            print(f"Color Temperature: {cct:.0f} K")
        except Exception:
            print("Color Temperature: unavailable")

        print("-" * 40)

    except RuntimeError:
        # CRC check failed while reading data - skip this sample
        pass
    except Exception as e:
        print(f"Error reading sensor data: {e}")
        print("-" * 40)

    time.sleep(1)
