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

    import sys
    sys.exit(1)

print("MCP9808 Temperature Sensor")
print("=" * 35)

# Display sensor information
print(f"Resolution: {mcp9808.resolution}°C")
print(f"Alert Temperature: {mcp9808.alert_temperature}°C")
print(f"Alert Hysteresis: {mcp9808.alert_hysteresis}°C")
print(f"Alert Mode: {mcp9808.alert_mode}")
print(f"Alert Polarity: {mcp9808.alert_polarity}")
print(f"Alert Status: {mcp9808.alert_status}")
print()

# Main reading loop
while True:
    try:
        temp = mcp9808.temperature
        
        print(f"Temperature: {temp:.1f}°C")
        print("-" * 30)
        
        time.sleep(30)
        
    except Exception as e:
        print(f"Error reading sensor: {e}")
        time.sleep(5)        print(f"Temperature: {temp:.2f}°C")
        
        # Determine temperature level
        if temp < 0:
            temp_level = "Freezing"
        elif temp < 10:
            temp_level = "Cold"
        elif temp < 20:
            temp_level = "Cool"
        elif temp < 30:
            temp_level = "Room Temperature"
        elif temp < 40:
            temp_level = "Warm"
        else:
            temp_level = "Hot"
            
        print(f"Temperature Level: {temp_level}")
        print("-" * 30)
        
        time.sleep(30)
        
    except Exception as e:
        print(f"Error reading sensor: {e}")
        time.sleep(5)
