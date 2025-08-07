## Usage

### Basic Usage

```bash
circremote [options] <serial_port or ip:port> <command_name> [command line options]
```

### Show Version
```bash
circremote --version
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
circremote -d /dev/ttyUSB0 info
```

#### WebSocket Connection (CircuitPython Web Workflow)
```bash
# Connect to CircuitPython device via IP
circremote 192.168.1.100 SHT30

# Connect with custom port
circremote 192.168.1.100:8080 settings

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
- `-C, --config PATH`: Path to circremote JSON config file (`~/.circremote/config.json` by default)
- `-l, --list`: List all available commands from all sources
- `-h, --help`: Show help message 
- `-h COMMAND`: Show help for a specific command
- `-t TIMEOUT: exit TIMEOUT seconds after sending the command - 0 to not exit`
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

`circremote` needs a way to communicate with the CircuitPython device that's going to run the code.

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

If you use ` https://example.com/sensor.py`, `circremote` will attempt to load `https://example.com/requirements.txt` and `https://example.com/info.json` - if they're present, it will process them as normal. If they're not, it will still attempt to run `sensor.py` on the device but will be unable to use `circup` to install any necessary libraries.

If you use `https://example.com/sensor` or `https://example.com/sensor/`, `circremote` will attempt to load `https://example.com/sensor/code.py`. If that succeeds, it will also attempt to load `https://example.com/sensor/requirements.txt` and `https://example.com/sensor/info.json` and will continue processing as described above.

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
