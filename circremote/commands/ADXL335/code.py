# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import analogio

# Initialize analog inputs for ADXL335
try:
    adxl_x = analogio.AnalogIn(board.A0)  # X-axis
    adxl_y = analogio.AnalogIn(board.A1)  # Y-axis
    adxl_z = analogio.AnalogIn(board.A2)  # Z-axis
except Exception as e:
    print(f"Error initializing ADXL335: {e}")
    import sys
    sys.exit(1)

# Reference voltage (usually 3.3V)
VCC = 3.3

print("ADXL335 Analog Accelerometer")
print("=" * 35)

# Display sensor information
print("Interface: Analog (3-axis)")
print("Range: ±3g")
print("Supply Voltage: 3.3V")
print("Output: 0.5V at 0g, 1.65V at 0g (ratiometric)")
print()

# Main reading loop
while True:
    # Read raw analog values
    x_raw = adxl_x.value
    y_raw = adxl_y.value
    z_raw = adxl_z.value
    
    # Convert to voltage
    x_voltage = (x_raw * VCC) / 65536
    y_voltage = (y_raw * VCC) / 65536
    z_voltage = (z_raw * VCC) / 65536
    
    # Convert to acceleration (assuming 3.3V supply and ±3g range)
    # 0g = 1.65V, 1g = 0.55V change
    x_accel = (x_voltage - 1.65) / 0.55
    y_accel = (y_voltage - 1.65) / 0.55
    z_accel = (z_voltage - 1.65) / 0.55
    
    # Calculate magnitude
    magnitude = (x_accel**2 + y_accel**2 + z_accel**2)**0.5
    
    # Display readings
    print(f"Raw X: {x_raw}")
    print(f"Raw Y: {y_raw}")
    print(f"Raw Z: {z_raw}")
    print()
    print(f"Voltage X: {x_voltage:.3f}V")
    print(f"Voltage Y: {y_voltage:.3f}V")
    print(f"Voltage Z: {z_voltage:.3f}V")
    print()
    print(f"Acceleration X: {x_accel:.2f} g")
    print(f"Acceleration Y: {y_accel:.2f} g")
    print(f"Acceleration Z: {z_accel:.2f} g")
    print(f"Magnitude: {magnitude:.2f} g")
    
    # Determine movement level
    if magnitude < 1.1:
        movement = "Stationary"
    elif magnitude < 1.5:
        movement = "Slight Movement"
    elif magnitude < 2.0:
        movement = "Moderate Movement"
    else:
        movement = "Strong Movement"
        
    print(f"Movement Level: {movement}")
    print("-" * 30)
    
    time.sleep(30) 
