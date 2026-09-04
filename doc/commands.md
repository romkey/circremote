# Available Commands

`circremote` comes with a collection of pre-built sensor and utility commands:

### Air Quality Sensors
- `CCS811` - Digital gas sensor for VOCs and eCO2
- `ENS160` - Digital gas sensor for VOCs, eCO2, and TVOC
- `PMS5003` - Particulate matter sensor 
- `PMSA003I` - I2C particulate matter sensor 
- `SCD30` - CO2, temperature, and humidity sensor
- `SCD40` - CO2, temperature, and humidity sensor
- `SCD43` - CO2, temperature, and humidity sensor with extended CO2 range
- `SEN54` - Multi-gas environmental sensor (temperature, humidity, VOC, NOx)
- `SEN55` - Comprehensive environmental sensor (temperature, humidity, VOC, NOx, PM)
- `SEN66` - Environmental sensor
- `SGP30` - Air quality sensor for eCO2 and TVOC
- `SGP40` - VOC air quality sensor
- `STCC4` - CO2, temperature, and humidity sensor

### Analog & Digital Converters
- `ADS7128` - 8-channel 12-bit ADC with GPIO, oversampling, and alerts
- `GP8403` - 2-channel 12-bit I2C DAC with 0-5V/0-10V output
- `PCF8591` - 8-bit ADC/DAC converter with 4 analog input channels and 1 analog output channel

### Light Sensors
- `APDS9301` - Digital light sensor with broadband and infrared detection
- `APDS9960` - Digital proximity, ambient light, RGB color, and gesture sensor
- `APDS9999` - Digital RGB, IR, and proximity sensor
- `AS7262` - Spectral sensor for color identification and material analysis
- `AS7341` - Multi-spectral color sensor
- `AS7343` - 14-channel multi-spectral sensor from violet to near-infrared
- `BH1750` - Digital light sensor 
- `LTR-303` - Digital light sensor
- `LTR-329` - Digital light sensor
- `LTR390` - UV light sensor 
- `MAX44009` - Ultra-low-power ambient light sensor with wide dynamic range
- `TCRT1000` - Reflective optical sensor
- `TCS3430` - XYZ tristimulus color sensor
- `TSL2561` - High-accuracy digital light sensor with light source identification
- `TSL2591` - High-dynamic-range digital light sensor
- `VCNL4030` - Proximity and ambient light sensor with integrated IR emitter
- `VEML7700` - High-accuracy ambient light sensor

### Magnetic Field Sensors
- `BNO055` - 9-axis absolute orientation sensor with integrated magnetometer
- `DRV5032` - Digital hall effect sensor for magnetic field detection
- `LIS2MDL` - 3-axis magnetometer
- `LIS3MDL` - 3-axis magnetometer
- `MMC5603` - 3-axis magnetometer with high resolution
- `MLX90393` - 3-axis magnetometer
- `TMAG5273A1` - 3D Hall effect sensor (±40/80 mT)
- `TMAG5273A2` - 3D Hall effect sensor (±133/266 mT)
- `TLV493D` - 3-axis magnetometer

### Motion & Position Sensors
- `ADXL335` - 3-axis analog accelerometer
- `ADXL343` - 3-axis accelerometer with high-resolution measurements
- `ADXL345` - 3-axis accelerometer with high resolution (13-bit)
- `ADXL375` - High-g accelerometer for impact detection (±200g)
- `BNO055` - 9-axis absolute orientation sensor with accelerometer, gyroscope, magnetometer, and fused orientation data
- `ISM330DHCX` - 6-axis IMU with high-performance accelerometer and gyroscope
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

### OneWire Interface
- `DS2484` - 1-Wire master controller for I2C to 1-Wire bridge functionality
- `DS248x` - Generic DS248x series 1-Wire master controller
- `onewire` - OneWire interface communication and device management

### Power & Energy Sensors
- `INA219` - High-side current shunt and power monitor with voltage, current, and power measurement

### Pressure & Altitude Sensors
- `BMP280` - Digital barometric pressure sensor
- `BMP388` - High-precision barometric pressure sensor
- `BMP390` - High-precision barometric pressure sensor for altitude measurement
- `DPS310` - Digital barometric pressure sensor
- `LPS22` - Digital barometric pressure sensor
- `LPS28DFW` - Digital barometric pressure sensor with FIFO buffer
- `MPL3115A2` - Digital barometric pressure sensor
- `MS6807` - Digital barometric pressure sensor

### Temperature & Humidity Sensors
- `ADT7410` - High-accuracy digital temperature sensor with ±0.5°C accuracy
- `AHT20` - Temperature and humidity sensor 
- `BME280` - Temperature, humidity, and pressure sensor
- `BME680` - Temperature, humidity, pressure, and gas sensor
- `BMP3XX` - Generic BMP3xx series barometric pressure and temperature sensor
- `DS18B20` - Digital temperature sensor using OneWire protocol
- `HDC3022` - High-accuracy temperature and humidity sensor 
- `HTU31` - Digital temperature and humidity sensor with ±0.2°C accuracy
- `PCT2075` - Digital temperature sensor with programmable temperature limits
- `SHT20` - Digital temperature and humidity sensor
- `SHT30` - High-accuracy temperature and humidity sensor
- `SHT31D` - Digital temperature and humidity sensor
- `SHT41` - High-precision digital temperature and humidity sensor
- `SHT45` - High-precision digital temperature and humidity sensor
- `SHTC3` - Digital temperature and humidity sensor with 16-bit resolution
- `Si7021` - Digital temperature and humidity sensor
- `TMP117` - High-accuracy digital temperature sensor
- `TMP119` - High-precision digital temperature sensor with ±0.03°C accuracy

### Thermal Imaging
- `AMG8833` - 8x8 thermal camera sensor for infrared temperature measurements
- `MLX90640` - Thermal imaging sensor

### Time & Real-Time Clock
- `DS3231` - High-accuracy real-time clock
- `PCF8523` - Real-time clock

### Utility Commands
- `analog-read` - Read analog values from a pin using ADC
- `benchmark` - Performance benchmark tool for testing computational operations (arithmetic, data structures, function calls)
- `blink` - Blinks a simple LED
- `ble-scan` - Scan for nearby Bluetooth devices and display their information
- `cat` - Display contents of a file
- `clean` - Clean unwanted files like ._file_, file~ and others from the device
- `digital-read` - Read digital values from a pin
- `digital-write` - Write digital values to a pin
- `enable-webworkflow` - Configure CircuitPython Web Workflow and WiFi on ESP32 devices (⚠️ can make device go offline)
- `erase-fs` - erase the filesystem - cannot be undone. Requires the  word `yes` as an argument. Restarts the device.
- `gps-serial` - Read and display NMEA GPS data from a serial GPS device
- `hello` - Hello world
- `info` - Display information about the board - CircuitPython version, pin definitions, free memory and flash, wifi info
- `ls` - List files and directories recursively
- `matrix-diagnostic` - Run comprehensive diagnostics on LED matrix displays
- `matrix-rainbow` - Display a marching rainbow effect on LED matrix displays
- `neopixel-blink` - Blinks a NeoPixel LED
- `neopixel-cylon` - Classic Cylon effect with red blob bouncing side to side
- `neopixel-rainbow` - Cycles through rainbow colors on a NeoPixel LED
- `neopixel-test` - Diagnostic test for neopixel arrays to identify pixel count issues
- `ntp` - Get the time from an NTP server 
- `ping` - Ping (ICMP Echo Request) another device
- `pwm-write` - Control PWM output on a pin
- `relay-serial` - Display received serial data
- `reset` - Restart the device (`microcontroller.reset()`)
- `rm` - Remove files and directories recursively
- `run` - Reads a file on the device and executes it
- `scan-i2c` - Scan for I2C devices 
- `scan-wifi` - Scan for WiFi networks 
- `settings` - Display contents of `settings.toml` (same as `cat settings.toml`) 
- `stop` - Park the device in an idle sleep loop (halts the running program)
- `uf2` - Restart compatible devices in UF2 bootloader mode (this will take the device offline if it's on wifi)
