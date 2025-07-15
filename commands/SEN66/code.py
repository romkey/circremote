# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_sen6x

print("SEN66 Environmental Sensor")
print("=" * 40)

# Initialize I2C bus (support template pins, fallback to board.I2C)
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except Exception:
    i2c = board.I2C()

# Initialize SEN66 sensor
try:
    sen66 = adafruit_sen6x.SEN66(i2c)
    print("✓ SEN66 sensor initialized successfully")
    print(f"Serial Number: {sen66.serial_number}")
except Exception as e:
    print(f"✗ Error initializing SEN66: {e}")
    import sys
    sys.exit(1)

print("\nStarting environmental measurements...")
print("Readings:")

while True:
    sen66.start_measurement()
    time.sleep(2)

    if sen66.data_ready:
        sen66.check_sensor_errors()

        data = sen66.all_measurements()
        
        print("All Measurements:")
        # Sort by key and format for display
        sorted_items = sorted(data.items())
        
        # Calculate display keys and max length
        display_keys = []
        for key, value in sorted_items:
            if key.startswith('pm'):
                display_key = 'PM' + key[2:].upper()
            else:
                # Manual capitalization for CircuitPython
                display_key = key[0].upper() + key[1:].lower()
            display_keys.append(display_key)
        
        max_key_length = max(len(display_key) for display_key in display_keys)
        
        for i, (key, value) in enumerate(sorted_items):
            display_key = display_keys[i]
            
            # Align the fields
            if isinstance(value, float):
                print(f"  {display_key:<{max_key_length}}: {value:.2f}")
            else:
                print(f"  {display_key:<{max_key_length}}: {value}")

    print("-" * 30)
    time.sleep(30)
