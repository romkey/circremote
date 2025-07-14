# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_pm25

# Initialize UART for PMS5003
try:
    uart = busio.UART({{ tx }}, {{ rx }}, baudrate=9600)
except:
    try:
        uart = busio.UART(board.TX, board.RX, baudrate=9600)
    except Exception as e:
        print(f"Error initializing PMS5003: {e}")
        import sys
        sys.exit(1)

# Initialize PM2.5 sensor
try:
    pms5003 = PMS5003(uart)
except Exception as e:
    print(f"Error initializing PMS5003: {e}")
    import sys
    sys.exit(1)

print("PMS5003 Particulate Matter Sensor")
print("=" * 40)

# Display sensor information
print("Sensor Type: PMS5003")
print("Interface: UART (9600 baud)")
print("Particle Size Range: 0.3 - 10 μm")
print()

# Main reading loop
while True:
    # Read sensor values
    aqdata = pm25.read()
        
    # Display readings
    print("PM1.0 Standard: {} μg/m³".format(aqdata["pm10 standard"]))
    print("PM2.5 Standard: {} μg/m³".format(aqdata["pm25 standard"]))
    print("PM10 Standard: {} μg/m³".format(aqdata["pm100 standard"]))
    print()
    print("PM1.0 Environmental: {} μg/m³".format(aqdata["pm10 env"]))
    print("PM2.5 Environmental: {} μg/m³".format(aqdata["pm25 env"]))
    print("PM10 Environmental: {} μg/m³".format(aqdata["pm100 env"]))
    print()
    print("Particles > 0.3μm: {} / 0.1L".format(aqdata["particles 03um"]))
    print("Particles > 0.5μm: {} / 0.1L".format(aqdata["particles 05um"]))
    print("Particles > 1.0μm: {} / 0.1L".format(aqdata["particles 10um"]))
    print("Particles > 2.5μm: {} / 0.1L".format(aqdata["particles 25um"]))
    print("Particles > 5.0μm: {} / 0.1L".format(aqdata["particles 50um"]))
    print("Particles > 10μm: {} / 0.1L".format(aqdata["particles 100um"]))
    print("-" * 30)
        
    time.sleep(30) 
