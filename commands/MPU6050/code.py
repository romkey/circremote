# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_mpu6050

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize MPU6050
try:
    mpu = adafruit_mpu6050.MPU6050(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing MPU6050: {e}")
    import sys
    sys.exit(1)

print("MPU6050 Accelerometer & Gyroscope")
print("=" * 35)

# Display sensor information
print(f"Accelerometer Range: {mpu.accelerometer_range}")
print(f"Gyroscope Range: {mpu.gyroscope_range}")
print(f"Filter Bandwidth: {mpu.filter_bandwidth}")
print()

# Main reading loop
while True:
    # Read accelerometer data
    accel_x, accel_y, accel_z = mpu.acceleration
    
    # Read gyroscope data
    gyro_x, gyro_y, gyro_z = mpu.gyro
    
    # Read temperature
    temp = mpu.temperature
    
    # Calculate accelerometer magnitude
    accel_magnitude = (accel_x**2 + accel_y**2 + accel_z**2)**0.5
    
    # Calculate gyroscope magnitude
    gyro_magnitude = (gyro_x**2 + gyro_y**2 + gyro_z**2)**0.5
    
    # Display readings
    print(f"Acceleration X: {accel_x:.2f} m/s²")
    print(f"Acceleration Y: {accel_y:.2f} m/s²")
    print(f"Acceleration Z: {accel_z:.2f} m/s²")
    print(f"Acceleration Magnitude: {accel_magnitude:.2f} m/s²")
    print()
    print(f"Gyroscope X: {gyro_x:.2f} rad/s")
    print(f"Gyroscope Y: {gyro_y:.2f} rad/s")
    print(f"Gyroscope Z: {gyro_z:.2f} rad/s")
    print(f"Gyroscope Magnitude: {gyro_magnitude:.2f} rad/s")
    print()
    print(f"Temperature: {temp:.1f}°C")
    
    # Determine movement level
    if accel_magnitude < 10.5:
        movement = "Stationary"
    elif accel_magnitude < 11.5:
        movement = "Slight Movement"
    elif accel_magnitude < 15:
        movement = "Moderate Movement"
    else:
        movement = "Strong Movement"
        
    print(f"Movement Level: {movement}")
    
    # Determine rotation level
    if gyro_magnitude < 0.1:
        rotation = "No Rotation"
    elif gyro_magnitude < 1.0:
        rotation = "Slow Rotation"
    elif gyro_magnitude < 5.0:
        rotation = "Moderate Rotation"
    else:
        rotation = "Fast Rotation"
        
    print(f"Rotation Level: {rotation}")
    print("-" * 30)
    
    time.sleep(30)
