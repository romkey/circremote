# SPDX-FileCopyrightText: 2026 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_tmp117

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize TMP119 (the TMP117 library also drives the TMP119)
try:
    tmp119 = adafruit_tmp117.TMP117(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing TMP119: {e}")
    import sys
    sys.exit(1)

print("TMP119 High-Precision Temperature Sensor")
print("=" * 40)

# Display sensor information
try:
    print(f"Serial Number: 0x{tmp119.serial_number:012X}")
except Exception:
    pass
print(f"Averaged Measurements: {adafruit_tmp117.AverageCount.string[tmp119.averaged_measurements]}x")
print(f"Measurement Delay: {adafruit_tmp117.MeasurementDelay.string[tmp119.measurement_delay]} s")
print(f"Temperature Offset: {tmp119.temperature_offset:.4f}°C")
print()

# Main reading loop
while True:
    try:
        temperature = tmp119.temperature

        print(f"Temperature: {temperature:.4f}°C")
        print(f"Temperature: {temperature * 9 / 5 + 32:.4f}°F")

        alert_status = tmp119.alert_status
        if alert_status.high_alert:
            print("High temperature alert active")
        if alert_status.low_alert:
            print("Low temperature alert active")

        print("-" * 30)

    except Exception as e:
        print(f"Error reading sensor data: {e}")
        print("-" * 30)

    time.sleep(1)
