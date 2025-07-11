# cpctrl

A command-line tool for uploading and running Python code on CircuitPython devices via serial or WebSocket connections, with support for dependency management and sensor libraries.

## Installation

### From PyPI

```bash
pip install cpctrl
```

### From Source

```bash
git clone https://github.com/yourusername/cpctrl-python.git
cd cpctrl-python
pip install -e .
```

## Usage

### Basic Usage

```bash
cpctrl [options] <serial_port_or_ip> <command_name>
```

### Examples

#### Serial Connection
```bash
# Run BME280 sensor code on serial port
cpctrl /dev/ttyUSB0 BME280

# Run with verbose output
cpctrl -v /dev/ttyACM0 VL53L1X

# Run with double exit (additional Ctrl+D)
cpctrl -d /dev/ttyUSB0 system-info
```

#### WebSocket Connection (CircuitPython Web Workflow)
```bash
# Connect to CircuitPython device via IP
cpctrl 192.168.1.100 SHT30

# Connect with custom port
cpctrl 192.168.1.100:8080 show-settings

# Connect with HTTP basic auth password
cpctrl -p mypassword 192.168.1.100 scan-i2c

# Combine options
cpctrl -v -d -p mypassword 192.168.1.100:8080 BME680
```

## Options

- `-v, --verbose`: Enable verbose debug output
- `-p, --password PASSWORD`: HTTP basic auth password for WebSocket connections
- `-d, --double-exit`: Send additional Ctrl+D after Ctrl+B to exit raw REPL
- `-y, --yes`: Skip confirmation prompts (run untested commands without asking)
- `-C, --skip-circup`: Skip circup dependency installation
- `-h, --help`: Show help message

## Available Commands

The tool comes with a collection of pre-built sensor and utility commands:

### Temperature & Humidity Sensors
- `BME280` - Temperature, humidity, and pressure sensor
- `BME680` - Temperature, humidity, pressure, and gas sensor
- `SHT30` - High-accuracy temperature and humidity sensor
- `SHT31D` - Digital temperature and humidity sensor
- `AHT20` - Temperature and humidity sensor
- `HDC3022` - High-accuracy temperature and humidity sensor

### Light Sensors
- `TSL2591` - High-dynamic-range digital light sensor
- `VEML7700` - High-accuracy ambient light sensor
- `BH1750` - Digital light sensor
- `LTR390` - UV light sensor

### Motion & Position Sensors
- `LIS3DH` - 3-axis accelerometer
- `LIS3MDL` - 3-axis magnetometer
- `LSM6DSOX` - 6-axis IMU (accelerometer + gyroscope)
- `MPU6050` - 6-axis motion tracking sensor
- `VL53L0X` - Time-of-flight distance sensor
- `VL53L1X` - Long-range time-of-flight sensor

### Air Quality Sensors
- `SCD40` - CO2, temperature, and humidity sensor
- `SGP30` - Air quality sensor
- `SGP40` - VOC air quality sensor
- `PMS5003` - Particulate matter sensor

### Utility Commands
- `system-info` - Display system information
- `scan-i2c` - Scan for I2C devices
- `scan_wifi` - Scan for WiFi networks
- `show-settings` - Display current settings
- `simple` - Simple test command

## Features

### Automatic Dependency Management
When a command has a `requirements.txt` file, cpctrl can automatically install CircuitPython libraries using `circup`:

- Detects if `circup` is available
- Prompts user to install dependencies
- Supports both serial and WebSocket connections for dependency installation
- Provides options to run, skip, or exit

### Safety Warnings
Commands can include safety warnings for potentially problematic code:

- Warns about modules that may make devices unreachable
- Explains potential risks (deep sleep, network disconnection, etc.)
- Requires user confirmation before proceeding

### Untested Module Warnings
Commands can be marked as untested:

- Warns about modules that haven't been tested
- Explains potential issues (wrong pins, addresses, etc.)
- Requires user confirmation unless `-y` flag is used

### Connection Types

#### Serial Connection
- Supports standard serial ports (USB, UART)
- Configurable baud rate (default: 115200)
- Cross-platform support

#### WebSocket Connection
- Supports CircuitPython Web Workflow
- HTTP basic authentication
- Automatic protocol detection (ws/wss)
- Configurable host and port

### Error Handling
- Comprehensive error reporting
- Graceful handling of connection failures
- Detailed debug output with verbose mode
- Automatic cleanup of connections

## Development

### Installing Locally

```bash
pip install -e .
```

### Running Tests

```bash
python -m pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- CircuitPython community for the excellent ecosystem
- Adafruit for the sensor libraries
- Python community for the package infrastructure 