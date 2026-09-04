# SPDX-FileCopyrightText: 2026 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_tmag5273

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize TMAG5273A2
try:
    tmag = adafruit_tmag5273.TMAG5273(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing TMAG5273A2: {e}")
    import sys
    sys.exit(1)

print("TMAG5273A2 3D Hall Effect Sensor")
print("=" * 40)

# Display sensor information
print(f"Manufacturer ID: 0x{tmag.manufacturer_id:04X}")
print(f"Device ID: 0x{tmag.device_id:02X}")
print(f"Wide XY Range: {tmag.xy_range_wide}")
print(f"Wide Z Range: {tmag.z_range_wide}")
print("Angle Calculation: XY plane")
print()

# Main reading loop
while True:
    try:
        mag_x, mag_y, mag_z = tmag.magnetic
        temperature = tmag.temperature
        angle = tmag.angle
        magnitude = tmag.magnitude_mt

        print(f"Magnetic X: {mag_x:.2f} uT")
        print(f"Magnetic Y: {mag_y:.2f} uT")
        print(f"Magnetic Z: {mag_z:.2f} uT")
        print(f"Angle (XY): {angle:.2f}°")
        print(f"Magnitude: {magnitude:.2f} mT")
        print(f"Temperature: {temperature:.1f}°C")
        print("-" * 30)

    except Exception as e:
        print(f"Error reading sensor data: {e}")
        print("-" * 30)

    time.sleep(1)
