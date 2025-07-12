# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_tmp117

print("TMP117 High-Precision Temperature Sensor")
print("=" * 40)

# Initialize I2C bus
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize TMP117 sensor
try:
    tmp117 = adafruit_tmp117.TMP117(i2c, address={{ address }})
    print("✓ TMP117 sensor initialized successfully")
    
except Exception as e:
    print(f"✗ Error initializing TMP117: {e}")
    import sys
    sys.exit(1)

print("\nStarting temperature measurements...")
print("Temperature readings (°C):")

while True:
    temperature = tmp117.temperature
    fahrenheit = temperature * 9/5 + 32
        
    print(f"Temperature: {temperature:.3f} °C ({fahrenheit:.3f} °F)")
    print("-" * 30)
        
    time.sleep(30)
