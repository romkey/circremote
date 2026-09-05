# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_ens160

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize ENS161. The Adafruit ENS160 library accepts both the ENS160
# (part ID 0x160) and the ENS161 (part ID 0x161).
try:
    ens = adafruit_ens160.ENS160(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing ENS161: {e}")
    import sys
    sys.exit(1)

print("ENS161 Air Quality Sensor")
print("=" * 30)

# Display sensor information
try:
    print(f"Part ID: 0x{ens.part_id:03X}")
except Exception:
    pass

try:
    print(f"Firmware Version: {ens.firmware_version}")
except Exception:
    pass
print()

# Compensate with room temperature and humidity. Set these from a real
# temperature/humidity sensor if you have one on the same bus.
try:
    ens.temperature_compensation = 25
    ens.humidity_compensation = 50
except Exception as e:
    print(f"Could not set compensation values: {e}")

print("Note: the sensor needs several minutes of warm-up before readings")
print("become valid. Data validity is reported with each measurement.")
print()

VALIDITY = {
    0: "Normal Operation",
    1: "Warm-Up",
    2: "Initial Start-Up",
    3: "Invalid Output",
}

# Main reading loop
while True:
    try:
        # Read sensor values
        aqi = ens.AQI
        tvoc = ens.TVOC
        eco2 = ens.eCO2
        validity = ens.data_validity

        # Display readings
        print(f"Air Quality Index: {aqi}")
        print(f"TVOC: {tvoc} ppb")
        print(f"eCO2: {eco2} ppm")
        print(f"Data Validity: {VALIDITY.get(validity, validity)}")
        print("-" * 30)

    except Exception as e:
        print(f"Error reading sensor data: {e}")
        print("-" * 30)

    time.sleep(30)
