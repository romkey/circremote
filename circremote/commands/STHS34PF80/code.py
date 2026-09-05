# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_sths34pf80

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize STHS34PF80
try:
    sths = adafruit_sths34pf80.STHS34PF80(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing STHS34PF80: {e}")
    import sys
    sys.exit(1)

print("STHS34PF80 IR Presence & Motion Sensor")
print("=" * 40)

# Display sensor configuration
try:
    print(f"Data Rate: {sths.data_rate}")
except Exception:
    pass

try:
    print(f"Gain Mode: {sths.gain_mode}")
except Exception:
    pass

try:
    print(f"Sensitivity: {sths.sensitivity}")
except Exception:
    pass
print()

print("Note: presence, motion and temperature shock are reported by the")
print("sensor's embedded algorithms. Object temperature values are raw")
print("LSB counts, not degrees.")
print("Readings:")
print()

# Main reading loop
while True:
    try:
        # Wait for a new sample rather than re-reading the same one
        if not sths.data_ready:
            time.sleep(0.1)
            continue

        # Temperature values
        ambient_temp = sths.ambient_temperature
        object_temp = sths.object_temperature
        comp_object_temp = sths.compensated_object_temperature

        # Algorithm outputs
        presence_val = sths.presence_value
        motion_val = sths.motion_value
        temp_shock_val = sths.temperature_shock_value

        # Detection flags
        presence = sths.presence
        motion = sths.motion
        temp_shock = sths.temperature_shock

        print(f"Ambient Temperature: {ambient_temp:.2f}°C")
        print(f"Object Temperature (raw): {object_temp}")
        print(f"Object Temperature (compensated): {comp_object_temp}")
        print(f"Presence: {presence_val}{' [DETECTED]' if presence else ''}")
        print(f"Motion: {motion_val}{' [DETECTED]' if motion else ''}")
        print(f"Temperature Shock: {temp_shock_val}{' [DETECTED]' if temp_shock else ''}")
        print("-" * 40)

    except Exception as e:
        print(f"Error reading sensor data: {e}")
        print("-" * 40)

    time.sleep(1)
