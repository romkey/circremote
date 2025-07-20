# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_bmp3xx

print("BMP388 Barometric Pressure Sensor")
print("=" * 40)

# Initialize I2C bus
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize BMP388 sensor
try:
    bmp388 = adafruit_bmp3xx.BMP3XX_I2C(i2c, address={{ address }})
    print("✓ BMP388 sensor initialized successfully")
    
    # Configure sensor settings
    bmp388.pressure_oversampling = 8
    bmp388.temperature_oversampling = 2
    bmp388.filter_coefficient = 2
    bmp388.output_data_rate = 4
    
    print(f"Pressure Oversampling: {bmp388.pressure_oversampling}")
    print(f"Temperature Oversampling: {bmp388.temperature_oversampling}")
    print(f"Filter Coefficient: {bmp388.filter_coefficient}")
    print(f"Output Data Rate: {bmp388.output_data_rate}")
    
except Exception as e:
    print(f"✗ Error initializing BMP388: {e}")
    import sys
    sys.exit(1)

print("\nStarting pressure and temperature measurements...")
print("Readings:")

# Main measurement loop
try:
    while True:
        # Read pressure and temperature
        pressure = bmp388.pressure
        temperature = bmp388.temperature
        
        # Calculate altitude (approximate)
        altitude = 44330 * (1.0 - (pressure / 101325.0) ** 0.1903)
        
        print(f"Pressure: {pressure:.2f} hPa")
        print(f"Temperature: {temperature:.2f} °C")
        print(f"Altitude: {altitude:.2f} m")
        print("-" * 30)
        
        time.sleep(30)  # Wait 30 seconds between readings
        
except KeyboardInterrupt:
    print("\nMeasurement stopped by user")
except Exception as e:
    print(f"\nError during measurement: {e}")

print("***END***") 
