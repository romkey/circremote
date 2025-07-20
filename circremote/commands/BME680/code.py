# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_bme680

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize BME680
try:
    bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, address={{ address }})

    # Configure BME680 for high accuracy
    bme680.sea_level_pressure = 1013.25  # Set sea level pressure in hPa
    bme680.gas_heater_temperature = 320  # Celsius
    bme680.gas_heater_duration = 150  # milliseconds
    bme680.gas_heater_profile = 0
except Exception as e:
    print(f"Error initializing BME680: {e}")
    import sys
    sys.exit(1)

print("BME680 Temperature, Humidity, Pressure & Gas Sensor")
print("=" * 55)

# Display sensor information
print(f"Temperature Oversample: {bme680.temperature_oversample}")
print(f"Humidity Oversample: {bme680.humidity_oversample}")
print(f"Pressure Oversample: {bme680.pressure_oversample}")
print(f"Filter Size: {bme680.filter_size}")
print(f"Gas Heater Temperature: {bme680.gas_heater_temperature}°C")
print(f"Gas Heater Duration: {bme680.gas_heater_duration} ms")
print(f"Gas Heater Profile: {bme680.gas_heater_profile}")
print(f"Sea Level Pressure: {bme680.sea_level_pressure} hPa")
print()

while True:
    temp = bme680.temperature
    humidity = bme680.humidity
    pressure = bme680.pressure
    altitude = bme680.altitude
    gas = bme680.gas
        
    print(f"Temperature: {temp:.1f}°C")
    print(f"Humidity: {humidity:.1f}%")
    print(f"Pressure: {pressure:.1f} hPa")
    print(f"Altitude: {altitude:.1f} m")
    print(f"Gas: {gas:.1f} kΩ")
    print("-" * 30)
        
    time.sleep(30)
