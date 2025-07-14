# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_bme280.advanced as adafruit_bme280

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize BME280
try:
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address={{ address }})

    # Configure BME280 for high accuracy
    bme280.sea_level_pressure = 1013.25  # Set sea level pressure in hPa
    bme280.mode = adafruit_bme280.MODE_NORMAL
    bme280.standby_period = adafruit_bme280.STANDBY_TC_500
    bme280.iir_filter = adafruit_bme280.IIR_FILTER_X16
except Exception as e:
    print(f"Error initializing BME280: {e}")
    import sys
    sys.exit(1)

print("BME280 Temperature, Humidity & Pressure Sensor")
print("=" * 50)

# Display sensor information
print(f"Temperature Resolution: {bme280.temperature_resolution}°C")
print(f"Pressure Resolution: {bme280.pressure_resolution} hPa")
print(f"Humidity Resolution: {bme280.humidity_resolution} %")
print(f"Sea Level Pressure: {bme280.sea_level_pressure} hPa")
print(f"Current Mode: {bme280.mode}")
print(f"Standby Period: {bme280.standby_period}")
print(f"IIR Filter: {bme280.iir_filter}")
print()

# Main reading loop
while True:
        # Read sensor values
        temp = bme280.temperature
        humidity = bme280.humidity
        pressure = bme280.pressure
        altitude = bme280.altitude
        
        # Display readings
        print(f"Temperature: {temp:.1f}°C")
        print(f"Humidity: {humidity:.1f}%")
        print(f"Pressure: {pressure:.1f} hPa")
        print(f"Altitude: {altitude:.1f} m")
        print("-" * 30)
        
        time.sleep(30)
