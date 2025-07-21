# circremote

A command-line tool for uploading and running Python code on CircuitPython devices via serial or WebSocket connections, with support for dependency management and sensor libraries.

## Installation

### From PyPI

```bash
pip install circremote
```

### From Source

```bash
git clone https://github.com/yourusername/circremote-python.git
cd circremote-python
pip install -e .
```

## Usage

### Basic Usage

```bash
circremote [options] <serial_port_or_ip> <command_name>
```

### Examples

#### Serial Connection
```bash
# Run BME280 sensor code on serial port
circremote /dev/ttyUSB0 BME280

# Run with verbose output
circremote -v /dev/ttyACM0 VL53L1X

# Run with double exit (additional Ctrl+D)
circremote -d /dev/ttyUSB0 system-info
```

#### WebSocket Connection (CircuitPython Web Workflow)
```bash
# Connect to CircuitPython device via IP
circremote 192.168.1.100 SHT30

# Connect with custom port
circremote 192.168.1.100:8080 show-settings

# Connect with HTTP basic auth password
circremote -p mypassword 192.168.1.100 scan-i2c

# Combine options
circremote -v -d -p mypassword 192.168.1.100:8080 BME680

# Skip dependency installation
circremote -C /dev/ttyUSB0 BME280

# Specify custom circup path
circremote -c /usr/local/bin/circup /dev/ttyUSB0 BME280
```

## Options

- `-v, --verbose`: Enable verbose debug output
- `-p, --password PASSWORD`: HTTP basic auth password for WebSocket connections
- `-d, --double-exit`: Send additional Ctrl+D after Ctrl+B to exit raw REPL
- `-y, --yes`: Skip confirmation prompts (run untested commands without asking)
- `-C, --skip-circup`: Skip circup dependency installation
- `-c, --circup PATH`: Path to circup executable
- `-l, --list`: List all available commands from all sources
- `-h, --help`: Show help message
- `-h COMMAND`: Show help for a specific command

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

## Configuration

### Device Shortcuts
Create a config file at `~/.circremote/config.json` to set up device shortcuts:

```json
{
  "devices": [
    {
      "name": "pico1",
      "device": "/dev/ttyACM0",
      "friendly_name": "Raspberry Pi Pico"
    },
    {
      "name": "feather1",
      "device": "192.168.1.100:8080",
      "password": "mypassword",
      "friendly_name": "Adafruit Feather ESP32"
    }
  ]
}
```

Then use the shortcut name:
```bash
circremote pico1 BME280
circremote feather1 BME280
```

### Command Aliases
Add command aliases to your config file:

```json
{
  "command_aliases": [
    {
      "name": "temp",
      "command": "BME280"
    },
    {
      "name": "light",
      "command": "TSL2591"
    }
  ]
}
```

Then use the alias:
```bash
circremote /dev/ttyUSB0 temp
```

### Search Paths
Add custom command directories to your config:

```json
{
  "search_paths": [
    "/path/to/my/commands",
    "~/custom_sensors",
    "/opt/circremote/commands"
  ]
}
```

Commands in these directories will be available by name:
```bash
circremote /dev/ttyUSB0 my_custom_sensor
```

The search order is:
1. Configured search paths (in order)
2. `~/.circremote/commands` (user commands)
3. Built-in commands

## Features

### Automatic Dependency Management
When a command has a `requirements.txt` file, circremote can automatically install CircuitPython libraries using `circup`:

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

### Custom Commands
You can create your own commands in several ways:

#### Python File Directly
Create a Python file and run it directly:
```bash
circremote /dev/ttyUSB0 ./my_sensor.py
```

#### Command Directory Structure
Create a directory with the required files:
```
my_command/
├── code.py          # Required: Your Python code
├── info.json        # Optional: Command metadata and variables
└── requirements.txt # Optional: Dependencies
```

Then run it:
```bash
circremote /dev/ttyUSB0 ./my_command
```

#### Using Search Paths
Add custom command directories to your config (see Configuration section above).

### Web Commands
Run commands directly from URLs:
```bash
# GitHub URLs (automatically converted to raw content)
circremote /dev/ttyUSB0 https://github.com/user/repo/blob/main/sensor.py

# Direct URLs
circremote /dev/ttyUSB0 https://example.com/sensor.py
```

### Error Handling
- Comprehensive error reporting
- Graceful handling of connection failures
- Detailed debug output with verbose mode
- Automatic cleanup of connections

## Getting Help

### General Help
```bash
circremote --help
```

### List All Commands
```bash
circremote -l
```

This shows all available commands from:
- Built-in commands
- Search path commands  
- User commands directory
- Command aliases (if configured)

### Command-Specific Help
```bash
# Show detailed help for any command
circremote -h BME280
circremote -h clean
circremote -h ./my_custom_command

# Shows:
# - Command description and location
# - Command line format
# - All arguments (required/optional)
# - Default values
# - Usage examples
```

### Debug Information
```bash
circremote -v /dev/ttyUSB0 BME280
```

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