# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_mlx90640

print("MLX90640 Thermal Camera Sensor")
print("=" * 40)

# Initialize I2C bus
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize MLX90640 sensor
try:
    mlx = adafruit_mlx90640.MLX90640(i2c, address={{ address }})
    print("✓ MLX90640 sensor initialized successfully")
    
    # Configure sensor settings
    mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ
    print(f"Refresh Rate: {mlx.refresh_rate}")
    
    # Get frame dimensions
    frame = [0] * 768
    print(f"Frame Size: {len(frame)} pixels (24x32)")
    
except Exception as e:
    print(f"✗ Error initializing MLX90640: {e}")
    import sys
    sys.exit(1)

print("\nStarting thermal imaging measurements...")
print("Temperature readings (°C):")

# Main measurement loop
try:
    while True:
        # Read thermal frame
        mlx.getFrame(frame)
        
        # Calculate statistics
        min_temp = min(frame)
        max_temp = max(frame)
        avg_temp = sum(frame) / len(frame)
        
        print(f"Min Temperature: {min_temp:.2f} °C")
        print(f"Max Temperature: {max_temp:.2f} °C")
        print(f"Average Temperature: {avg_temp:.2f} °C")
        
        # Display a simple 8x8 grid of the center area
        print("Center 8x8 Temperature Grid (°C):")
        for row in range(12, 20):  # Center rows
            row_data = []
            for col in range(12, 20):  # Center columns
                temp = frame[row * 32 + col]
                row_data.append(f"{temp:5.1f}")
            print(" ".join(row_data))
        
        print("-" * 30)
        time.sleep(30)  # Wait 30 seconds between readings
        
except KeyboardInterrupt:
    print("\nMeasurement stopped by user")
except Exception as e:
    print(f"\nError during measurement: {e}") 
