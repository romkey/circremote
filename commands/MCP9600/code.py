# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_mcp9600

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize MCP9600
try:
    mcp9600 = adafruit_mcp9600.MCP9600(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing MCP9600: {e}")
    import sys
    sys.exit(1)

print("MCP9600 Thermocouple Interface")
print("=" * 35)

# Display sensor information
print(f"Thermocouple Type: {mcp9600.thermocouple_type}")
print(f"Filter Coefficient: {mcp9600.filter_coefficient}")
print(f"ADC Resolution: {mcp9600.adc_resolution}")
print(f"Alert 1 Temperature: {mcp9600.alert1_temperature}°C")
print(f"Alert 2 Temperature: {mcp9600.alert2_temperature}°C")
print(f"Alert 3 Temperature: {mcp9600.alert3_temperature}°C")
print(f"Alert 4 Temperature: {mcp9600.alert4_temperature}°C")
print()

# Main reading loop
while True:
    temp = mcp9600.temperature
    hot_junction = mcp9600.hot_junction_temperature
    cold_junction = mcp9600.cold_junction_temperature
    delta_t = mcp9600.temperature_delta
    
    print(f"Temperature: {temp:.1f}°C")
    print(f"Hot Junction: {hot_junction:.1f}°C")
    print(f"Cold Junction: {cold_junction:.1f}°C")
    print(f"Delta Temperature: {delta_t:.1f}°C")
    
    # Determine temperature level
    if hot_junction < 0:
        temp_level = "Freezing"
    elif hot_junction < 50:
        temp_level = "Cold"
    elif hot_junction < 100:
        temp_level = "Warm"
    elif hot_junction < 200:
        temp_level = "Hot"
    elif hot_junction < 500:
        temp_level = "Very Hot"
    else:
        temp_level = "Extreme"
        
    print(f"Temperature Level: {temp_level}")
    print("-" * 30)
    
    time.sleep(30)
