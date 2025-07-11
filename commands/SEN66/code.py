# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_pm25


print("SEN66 Particulate Matter Sensor")
print("=" * 40)

# Initialize UART for SEN66 sensor
try:
    uart = busio.UART(board.TX, board.RX, baudrate=9600)
except Exception as e:
    print(f"Error initializing SEN66: {e}")
    import sys
    sys.exit(1)

# Initialize SEN66 sensor
try:
    pm25 = adafruit_pm25.PM25_UART(uart)
    print("✓ SEN66 sensor initialized successfully")
    
except Exception as e:
    print(f"✗ Error initializing SEN66: {e}")
    import sys
    sys.exit(1)

print("\nStarting particulate matter measurements...")
print("PM readings (μg/m³):")

# Main measurement loop
try:
    while True:
        # Read particulate matter data
        aqdata = pm25.read()
        
        if aqdata is not None:
            print(f"PM1.0: {aqdata['pm10 standard']} μg/m³")
            print(f"PM2.5: {aqdata['pm25 standard']} μg/m³")
            print(f"PM10: {aqdata['pm100 standard']} μg/m³")
            print(f"Particles >0.3μm: {aqdata['particles 03um']}")
            print(f"Particles >0.5μm: {aqdata['particles 05um']}")
            print(f"Particles >1.0μm: {aqdata['particles 10um']}")
            print(f"Particles >2.5μm: {aqdata['particles 25um']}")
            print(f"Particles >5.0μm: {aqdata['particles 50um']}")
            print(f"Particles >10μm: {aqdata['particles 100um']}")
        else:
            print("No data available")
        
        print("-" * 30)
        time.sleep(30)  # Wait 30 seconds between readings
        
except KeyboardInterrupt:
    print("\nMeasurement stopped by user")
except Exception as e:
    print(f"\nError during measurement: {e}") 
