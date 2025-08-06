# Available Commands

The tool comes with a collection of pre-built sensor and utility commands:

### Temperature & Humidity Sensors
- `AHT20` - Temperature and humidity sensor 
- `BME280` - Temperature, humidity, and pressure sensor
- `BME680` - Temperature, humidity, pressure, and gas sensor
- `HDC3022` - High-accuracy temperature and humidity sensor 
- `SHT30` - High-accuracy temperature and humidity sensor
- `SHT31D` - Digital temperature and humidity sensor

### Light Sensors
- `BH1750` - Digital light sensor 
- `LTR390` - UV light sensor 
- `TSL2591` - High-dynamic-range digital light sensor
- `VEML7700` - High-accuracy ambient light sensor

### Motion & Position Sensors
- `LIS3DH` - 3-axis accelerometer
- `LIS3MDL` - 3-axis magnetometer
- `LSM6DSOX` - 6-axis IMU (accelerometer + gyroscope)
- `MPU6050` - 6-axis motion tracking sensor
- `VL53L0X` - Time-of-flight distance sensor
- `VL53L1X` - Long-range time-of-flight sensor

### Air Quality Sensors
- `PMS5003` - Particulate matter sensor 
- `PMSA003I` - I2C particulate matter sensor 
- `SCD40` - CO2, temperature, and humidity sensor
- `SGP30` - Air quality sensor
- `SGP40` - VOC air quality sensor

### Utility Commands
- `blink` - blinks a simple LED
- `cat` - cat a file
- `clean` - clean unwanted files like ._file_, file~ and others from the device
-  `hello` - Hello world
- `neopixel-blink` - blinks a NeoPixel LED
- `neopixel-rainbow` - cycles through rainbow colors on a NeoPixel LED
- `ntp` - get the time from an NTP server
- `ping` - ping (ICMP Echo Request) another device
- `reset` - restart the device (`microcontroller.reset()`)
- `run` - reads a file on the device and executes it
- `scan-i2c` - Scan for I2C devices 
- `scan-wifi` - Scan for WiFi networks 
- `settings` - Display contents of `settings.toml` (same as `cat settings.toml`) 
- `system-info` - Display system information
- `uf2` - restart compatible devices in UF2 bootloader mode (this will take the device offline if it's on wifi)
