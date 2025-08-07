# Available Commands

`circremote` comes with a collection of pre-built sensor and utility commands:

### Temperature & Humidity Sensors
- `ADT7410` - High-accuracy digital temperature sensor with ±0.5°C accuracy
- `AHT20` - Temperature and humidity sensor 
- `BME280` - Temperature, humidity, and pressure sensor
- `BME680` - Temperature, humidity, pressure, and gas sensor
- `DS18B20` - Digital temperature sensor using OneWire protocol
- `HDC3022` - High-accuracy temperature and humidity sensor 
- `HTU31` - Digital temperature and humidity sensor with ±0.2°C accuracy
- `SHT20` - Digital temperature and humidity sensor
- `SHT30` - High-accuracy temperature and humidity sensor
- `SHT31D` - Digital temperature and humidity sensor
- `SHT41` - High-precision digital temperature and humidity sensor
- `SHT45` - High-precision digital temperature and humidity sensor
- `SHTC3` - Digital temperature and humidity sensor with 16-bit resolution
- `Si7021` - Digital temperature and humidity sensor
- `TMP117` - High-accuracy digital temperature sensor

### Light Sensors
- `APDS9960` - Digital proximity, ambient light, RGB color, and gesture sensor
- `AS7341` - Multi-spectral color sensor
- `BH1750` - Digital light sensor 
- `LTR-303` - Digital light sensor
- `LTR-329` - Digital light sensor
- `LTR390` - UV light sensor 
- `TCRT1000` - Reflective optical sensor
- `TSL2591` - High-dynamic-range digital light sensor
- `VEML7700` - High-accuracy ambient light sensor

### Motion & Position Sensors
- `ADXL335` - 3-axis analog accelerometer
- `ADXL343` - 3-axis accelerometer with high-resolution measurements
- `ADXL345` - 3-axis accelerometer with high resolution (13-bit)
- `ADXL375` - High-g accelerometer for impact detection (±200g)
- `LIS2MDL` - 3-axis magnetometer for compass applications
- `LIS3DH` - 3-axis accelerometer
- `LIS3MDL` - 3-axis magnetometer
- `LSGD20H` - 3-axis gyroscope
- `LSM63SDTR-C` - 6-axis IMU (accelerometer + gyroscope)
- `LSM6DSO32` - 6-axis IMU with machine learning core
- `LSM6DSOX` - 6-axis IMU (accelerometer + gyroscope)
- `MPU6050` - 6-axis motion tracking sensor
- `MSA311` - 3-axis accelerometer with motion detection
- `VL53L0X` - Time-of-flight distance sensor
- `VL53L1X` - Long-range time-of-flight sensor
- `VL53L4CX` - Advanced time-of-flight distance sensor
- `VL6180X` - Time-of-flight distance sensor with ambient light sensing

### Pressure & Altitude Sensors
- `BMP280` - Digital barometric pressure sensor
- `BMP388` - High-precision barometric pressure sensor
- `BMP390` - High-precision barometric pressure sensor for altitude measurement
- `DPS310` - Digital barometric pressure sensor
- `LPS22` - Digital barometric pressure sensor
- `LPS28DFW` - Digital barometric pressure sensor with FIFO buffer
- `MPL3115A2` - Digital barometric pressure sensor
- `MS6807` - Digital barometric pressure sensor

### Air Quality Sensors
- `CCS811` - Digital gas sensor for VOCs and eCO2
- `ENS160` - Digital gas sensor for VOCs, eCO2, and TVOC
- `PMS5003` - Particulate matter sensor 
- `PMSA003I` - I2C particulate matter sensor 
- `SCD30` - CO2, temperature, and humidity sensor
- `SCD40` - CO2, temperature, and humidity sensor
- `SEN54` - Multi-gas environmental sensor (temperature, humidity, VOC, NOx)
- `SEN55` - Comprehensive environmental sensor (temperature, humidity, VOC, NOx, PM)
- `SEN66` - Environmental sensor
- `SGP30` - Air quality sensor for eCO2 and TVOC
- `SGP40` - VOC air quality sensor

### Magnetic Field Sensors
- `DRV5032` - Digital hall effect sensor for magnetic field detection
- `LIS2MDL` - 3-axis magnetometer
- `LIS3MDL` - 3-axis magnetometer
- `MMC5603` - 3-axis magnetometer with high resolution
- `MLX90393` - 3-axis magnetometer
- `TLV493D` - 3-axis magnetometer

### Thermal Imaging
- `AMG8833` - 8x8 thermal camera sensor for infrared temperature measurements
- `MLX90640` - Thermal imaging sensor

### Time & Real-Time Clock
- `DS3231` - High-accuracy real-time clock
- `PCF8523` - Real-time clock

### Utility Commands
- `blink` - Blinks a simple LED
- `cat` - Display contents of a file
- `clean` - Clean unwanted files like ._file_, file~ and others from the device
- `hello` - Hello world
- `info` - Display information about the board - CircuitPython version, pin definitions, free memory and flash, wifi info
- `neopixel-blink` - Blinks a NeoPixel LED
- `neopixel-rainbow` - Cycles through rainbow colors on a NeoPixel LED
- `ntp` - Get the time from an NTP server 
- `ping` - Ping (ICMP Echo Request) another device
- `relay-serial` - Display received serial data
- `reset` - Restart the device (`microcontroller.reset()`)
- `run` - Reads a file on the device and executes it
- `scan-i2c` - Scan for I2C devices 
- `scan-wifi` - Scan for WiFi networks 
- `settings` - Display contents of `settings.toml` (same as `cat settings.toml`) 
- `uf2` - Restart compatible devices in UF2 bootloader mode (this will take the device offline if it's on wifi)

### OneWire Interface
- `DS2484` - 1-Wire master controller for I2C to 1-Wire bridge functionality
