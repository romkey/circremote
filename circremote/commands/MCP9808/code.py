# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_mcp9808

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize MCP9808
try:
    mcp9808 = adafruit_mcp9808.MCP9808(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing MCP9808: {e}")
    import sys
    sys.exit(1)

print("MCP9808 Temperature Sensor")
print("=" * 35)

# Display sensor information
print(f"Resolution: {mcp9808.resolution}°C")
print()

# Main reading loop
while True:
    temp = mcp9808.temperature
        
    print(f"Temperature: {temp:.1f}°C")
    print("-" * 30)
        
    time.sleep(30)
