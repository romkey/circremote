# circremote

A command-line tool for uploading and running Python code on CircuitPython devices via serial or Web Workflow websocket connections, with support for dependency management and sensor libraries.

## About This Project

I've been wanting a tool like circremote for quite a while. I have CircuitPython devices which are long running but which occasionally I'd like to run a diagnostic on. I also often bring up new sensors or test hardware using CircuitPython - I've run an I2C scanner countless times and always end up copying and pasting the code. circremote allows me to run code on the device without disturbing whatever is installed on it, and lets me very conveniently reuse code across devices and time. It lets me focus on managing the code rather than the device.

While I wanted a tool like this I was also busy and didn't feel like writing it. I'm a competent Python programmer but idiomatic Python isn't intuitive to me yet and while I'm enthusiastic about Python (and particularly CircuitPython) I'm not skilled enough to call myself a Pythonista.

And being a developer, I fundamentally want to do more with less.

Like many experienced developers, I've tried using LLMs to write code. My first results were poor, to put it kindly. The LLMs were not well trained in the areas I was working in. I asked for an ESP32 program and they hallucinated Adafruit libraries that didn't exist. The code didn't even compile. But the rate at which LLMs are improving is incredible. What was difficult for an LLM a few months ago it may now do flawlessly.

A friend was very excited about Cursor, so I decided that I'd try it out. The results were suprisingly good. My first go at it never got Web Workflow's websocket support in Python working but many other functions worked well. I'm more proficient in Ruby so I had Cursor rewrite circremote in Ruby, and it got websockets with the Web Workflow right on the first try. So I continued to iterate on the design in Ruby but the idea of telling the CircuitPython community that they needed to install Ruby in order to run circremote felt absurd. So I asked Cursor to rewrite it in Python again and it worked! Even the websocket support for Web Workflow.

This has been such a positive experience that it's really shifted my view on using an LLM to write code.

It also leaves me very concerned about maintenance. Fundamentally I designed this code but I didn't write it. I don't know it very well. I've gone down some rabbit holes with Cursor trying to correct bugs... and generally it's been okay but sometimes it goes down a dead end and builds up more and more cruft in the code with failed attempts... unwinding that can be tedious and difficult. Good git hygiene helps a lot but it's still too easy to end up with some twisted code from misugided attempts to fix things which never pan out.

I'm happy to say that almost all of the code and text in circremote was written by Cursor under my guidance. I've tweaked  the code directly here and there (mostly in some of the commands where Cursor was really not having a good time, and in parts of the text like this chunk and other places where there were nuances and useful information that Cursor just didn't get a grip on.

## Overview

This project maintains a set of snippets of CircuitPython code - things like an I2C scanner, a program which cleans up unwanted files left by text editors and operating systems, code for a large variety of sensors which will output the sensor's current readings, and other small programs. It can interrupt a program currently running on a CircuitPython device and transmit and execute this code over a USB serial connection. It also works with CircuitPython devices that are configured to use the "Web Workflow", which allows you to access files and run code over a small HTTP server that CircuitPython itself manages - so you can run code on a remote CircuitPython device that you're not physically connected to.

The snippets can include dependencies; each has its own `requirements.txt` file and circremote can automatically use `circup` to install those dependencies either locally to `CIRCUITPY` or over a network using the Web Workflow.

It can also pull code from a web server, so you can run Adafruit example code directly from Github if you want.

It supports a search path for code locations, so you can define your own or use other people's libraries, and fall back to the ones bundled with circremote.

One thing it currently does not do is support Microsoft Windows. I do not have a Windows machine and have no way to test it with Windows. I understand that a lot of people use Windows and that the lack of support means that a lot of people who might benefit from circremote won't be able to use it. While I'm happy to spend some time and resources on continuing to develop circremote and support users, I don't have the time, energy or desire to bring up a new platform and get it working on it. If a motivated co-maintainer comes along who'd like to get circremote working properly with Windows and then support it, I'd be happy to bring someone like that onto the project.

From here, see how to install circremote and then please check out the [FAQ](FAQ.md) to see how to use it.

## Installation

### From PyPI

```bash
pip install circremote
```

### From Source

```bash
git clone https://github.com/romkey/circremote
cd circremote-python
pip install -e .
```

## Usage

### Basic Usage

```bash
circremote [options] <serial_port_or_ip:port> <command_name>
```

### Show Version
```bash
circremote --version
# or
circremote -V
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
- `-f, --config PATH`: Path to circremote.json config file
- `-l, --list`: List all available commands from all sources
- `-h, --help`: Show help message
- `-h COMMAND`: Show help for a specific command
- `-V, --version`: Show version and exit

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
- `PMSA003I` - I2C particulate matter sensor

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
- `show-settings` - Display contents of `settings.toml` (same as `cat settings.toml`) 
- `system-info` - Display system information
- `uf2` - restart compatible devices in UF2 bootloader mode (this will take the device offline if it's on wifi)

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
# Run all tests (quiet mode with graceful interruption)
python -m pytest

# Run with custom test runner (recommended for better interruption handling)
python run_tests.py

# Run specific test categories
python -m pytest tests/unit/
python -m pytest tests/functional/
python -m pytest tests/integration/

# Run with verbose output (if needed)
python -m pytest -v

# Run with coverage
python -m pytest --cov=circremote --cov-report=html
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
