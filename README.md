# circremote

A command-line tool for uploading and running Python code on CircuitPython devices via serial or Web Workflow websocket connections, with support for dependency management and sensor libraries.

## Overview

This project maintains a set of snippets of CircuitPython code - things like an I2C scanner, a program which cleans up unwanted files left by text editors and operating systems, code for a large variety of sensors which will output the sensor's current readings, and other small programs. It can interrupt a program currently running on a CircuitPython device and transmit and execute this code over a USB serial connection. It also works with CircuitPython devices that are configured to use the "Web Workflow", which allows you to access files and run code over a small HTTP server that CircuitPython itself manages - so you can run code on a remote CircuitPython device that you're not physically connected to.

The snippets can include dependencies; each has its own `requirements.txt` file and circremote can automatically use `circup` to install those dependencies either locally to `CIRCUITPY` or over a network using the Web Workflow.

It can also pull code from a web server, so you can run Adafruit example code directly from Github if you want.

It supports a search path for code locations, so you can define your own or use other people's libraries, and fall back to the ones bundled with circremote.

One thing it currently does not do is support Microsoft Windows. I do not have a Windows machine and have no way to test it with Windows. I understand that a lot of people use Windows and that the lack of support means that a lot of people who might benefit from circremote won't be able to use it. While I'm happy to spend some time and resources on continuing to develop circremote and support users, I don't have the time, energy or desire to bring up a new platform and get it working on it. If a motivated co-maintainer comes along who'd like to get circremote working properly with Windows and then support it, I'd be happy to bring someone like that onto the project.

From here, see how to install circremote and then please check out the [FAQ](doc/FAQ.md) to see how to use it.

- [About circremote](doc/about.md)
- [Commands](doc/commands.md)
- [Configuration](doc/configuration.md)
- [Contributing](doc/contributing.md)

## Installation

### ~~From PyPI~~

(Not yet listed on PyPl so try "From Github" instead)

```bash
pip install circremote
```

### From Github
```
pip install git+https://github.com/romkey/circremote
```

### From Source

```bash
git clone https://github.com/romkey/circremote
cd circremote-python
pip install -e .
```

### Using Docker

**Note: running circup is not currently working correctly in the Docker image**

```bash
# Build the Docker image (includes circup for dependency management)
docker build -f docker/Dockerfile -t circremote:latest .

# Run circremote in a container with a serial port
CIRCREMOTE_SERIAL=/dev/ttyUSB0 docker-compose -f docker/docker-compose.yml run circremote-serial /dev/ttyUSB0 BME280

# Run circremote in a container with a networked device
docker-compose -f docker/docker-compose.yml run circremote 192.168.1.100 -p PASSWORD  BME280

# Test circup installation
docker run --rm circremote:latest circup --version

# For more Docker options, see [docker/README.md](docker/README.md)
```

## Usage

### Basic Usage

```bash
circremote [options] <serial_port or ip:port> <command_name> [command line options]
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
circremote -c /dev/ttyUSB0 BME280

# Specify custom circup path
circremote -u /usr/local/bin/circup /dev/ttyUSB0 BME280
```
## Options

- `-v, --verbose`: Enable verbose debug output
- `-p, --password PASSWORD`: HTTP basic auth password for WebSocket connections
- `-d, --double-exit`: Send additional Ctrl+D after Ctrl+B to exit raw REPL
- `-y, --yes`: Skip confirmation prompts (run untested commands without asking)
- `-c, --skip-circup`: Skip circup dependency installation
- `-u, --circup PATH`: Path to circup executable
- `-C, --config PATH`: Path to circremote.json config file
- `-l, --list`: List all available commands from all sources
- `-h, --help`: Show help message
- `-h COMMAND`: Show help for a specific command
- `-V, --version`: Show version and exit

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

circremote needs a way to communicate with the CircuitPython device that's going to run the code.

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
Running directly will not allow you to use variables, define a command line or have libraries automatically installed.

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

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- CircuitPython community for the excellent ecosystem
- Adafruit for the sensor libraries
- Python community for the package infrastructure 
