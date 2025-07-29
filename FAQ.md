# circremote FAQ

## General Questions

### What is circremote?
circremote is a command-line tool for uploading and running Python code on CircuitPython devices. It supports both local serial connections and networked WebSocket connections (via CircuitPython Web Workflow), making it easy to remotely control and run programs on CircuitPython boards.

### How do I install circremote?

```bash
pip install git+https://github.com/romkey/circremote
```

*Note this does not yet work as we're not yet listed in PyPI, for now please use the development install)*
```bash
pip install circremote
```

For development, you can install in editable mode:
```bash
git clone https://github.com/romkey/circremote
cd circremote-python
pip install -e .
```

### How do I use circremote under Windows?

I do not have access to a Windows machine and have not tried to use circremote on one. I cannot make any promises or offer any support for Windows users, sorry.

### What devices does circremote support?
circremote works with any CircuitPython-compatible board, including:
- Raspberry Pi Pico
- Adafruit Feather boards
- ESP32/ESP8266 boards
- SAMD21/SAMD51 boards
- And many others

## Command Usage

### How do I run a basic command?
```bash
circremote /dev/ttyUSB0 BME280
```

### How do I specify variables for a command?
```bash
# Explicit variable assignment
circremote /dev/ttyUSB0 BME280 sda=board.IO1 scl=board.IO2

# Positional arguments (if defined in info.json)
circremote /dev/ttyUSB0 mycommand board.IO1 board.IO2

# Mix of both
circremote /dev/ttyUSB0 mycommand board.IO1 board.IO2 address=0x76
```

### How do I connect to a device over WiFi?

You *must* configure the device to support [Web Workflow](https://learn.adafruit.com/getting-started-with-web-workflow-using-the-code-editor) in order to connect over WiFi. Only devices with integrated WiFi (ESP32s, Raspberry Pi Pico W) support Web Workflow. Devices using an external ESP32 as a WiFi coprocessor, like the Adafruit Matrix Portal M4 - this is a limitation of CircuitPython.

```bash
# Using IP address (default port 80)
circremote 192.168.1.100 BME280

# Using IP address with custom port
circremote 192.168.1.100:8080 BME280

# With password
circremote -p mypassword 192.168.1.100 BME280
```

### How do I enable verbose output?
```bash
circremote -v /dev/ttyUSB0 BME280
```

### How do I skip dependency installation?
```bash
circremote -c /dev/ttyUSB0 BME280
```

### How do I specify a custom circup path?
```bash
# Command line option
circremote -u /usr/local/bin/circup /dev/ttyUSB0 BME280
circremote -u ~/venv/bin/circup /dev/ttyUSB0 BME280

# Config file option
```

Add to your `~/.circremote/config.json`:
```json
{
  "circup": "/usr/local/bin/circup"
}
```

**Precedence order:**
1. Command line option (`-u PATH`) - highest priority
2. Config file setting (`"circup": "PATH"`)

### How do I use a custom config file?
```bash
# Use a different config file
circremote -C /path/to/custom.json /dev/ttyUSB0 BME280
circremote -C ~/projects/my_config.json 192.168.1.100 BME280

# Useful for:
# - Testing different configurations
# - Using different device sets for different projects
# - Sharing configurations with team members
```
3. System PATH resolution (`circup`) - default

### How do I set a timeout for output?
```bash
# Wait 30 seconds for output
circremote -t 30 /dev/ttyUSB0 BME280

# Wait indefinitely
circremote -t 0 /dev/ttyUSB0 BME280
```

## Device Configuration

### How do I set up shortcut names for devices?
Create a config file at `~/.circremote/config.json`:

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

### How do I set up command aliases?
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

## Custom Commands

### How do I create my own commands?
You can create commands in several ways:

#### 1. Python file directly
Create a Python file and run it directly:
```bash
circremote /dev/ttyUSB0 ./my_sensor.py
```

#### 2. Command directory structure
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

#### 3. Using search paths
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

### What should I include in info.json?
```json
{
  "name": "My Custom Sensor",
  "description": "A custom temperature and humidity sensor",
  "tested": true,
  "variables": [
    {
      "name": "sda",
      "description": "I2C SDA pin",
      "default": "board.SDA"
    },
    {
      "name": "scl", 
      "description": "I2C SCL pin",
      "default": "board.SCL"
    }
  ],
  "default_commandline": "sda scl"
}
```

### How do I use template variables in my code?
In your `code.py`, use `{{variable_name}}` syntax:
```python
import board
import busio
from adafruit_bme280 import basic as adafruit_bme280

# These will be replaced with actual values
i2c = busio.I2C({{scl}}, {{sda}})
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

print(f"Temperature: {bme280.temperature}°C")
```

## Loading Commands from the Web
circremote is able to download code from a web server and send it to a CircuitPython device. It currently only downloads the code; it cannot handle library dependencies or get information about the code from an `info.json` file.

Please be careful downloading random code from a web site. Even on a CircuitPython device it could contain malicious code which could share your WiFi credentials or other information stored on the device with bad actors.

### How do I run a command from GitHub?
circremote automatically rewrites Github URLs to properly access the file managed at that URL. These two examples are identical:

```bash
# Direct GitHub URL
circremote /dev/ttyUSB0 https://github.com/adafruit/Adafruit_CircuitPython_BME680/blob/main/examples/bme680_simpletest.py`

# GitHub raw URL
circremote /dev/ttyUSB0 https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_BME680/main/examples/bme680_simpletest.py
```

Be aware that circremote will not automatically install the BME680 library if you run this code this way. It will if you run the local `BME680` command.

### How do I run a command from other websites?
```bash
# Any HTTP/HTTPS URL
circremote /dev/ttyUSB0 https://romkey.com/circup/hello.py
```

### Can I use GitHub URLs with directories?
No, circremote does not currently support remote directories or remote `info.json` or `requirements.txt` files.

## Troubleshooting

### "Command not found" error
This usually means:
1. The command name is misspelled
2. The command doesn't exist in the built-in library
3. The command isn't in your search paths

Check available commands:
```bash
circremote -l
```

### "Connection refused" error
For serial connections:
- Check if the device is connected
- Verify the port name (e.g., `/dev/ttyUSB0`, `/dev/ttyACM0`)
- Make sure no other program is using the port

For WebSocket connections:
- Verify the IP address and port
- Check if CircuitPython [Web Workflow](https://learn.adafruit.com/getting-started-with-web-workflow-using-the-code-editor) is enabled on the device
- Ensure the device is on the same network

### "Bad password" error
For WebSocket connections:
- Check your password in the config or `-p` option
- Verify the password matches `CIRCUITPY_WEB_API_PASSWORD` in `settings.toml` on the device
- Restart the device after changing the password

### "Permission denied" error
For serial connections:
- Add your user to the `dialout` group (Linux):
  ```bash
  sudo usermod -a -G dialout $USER
  ```
- On macOS, you might need to install drivers for your device

### "Module not found" error
This means a required library isn't installed on the device:
1. Check if the command has a `requirements.txt` file
2. Make sure circup is installed: `pip install circup`
3. Try running without `-C` flag to install dependencies automatically

### "Template variables found but no variables available"
Your code uses template variables (like `{{sda}}`) but no values were provided:
```bash
# Provide values on command line
circremote /dev/ttyUSB0 BME280 sda=board.IO1 scl=board.IO2

# Or define defaults in info.json
```

### "Invalid variables provided" error
You provided a variable that isn't defined in the command's `info.json`:
1. Check the command's documentation for valid variables
2. Look at the `info.json` file to see what variables are expected
3. Use `-v` flag to see debug information

### "Circup not found" error
Install circup to manage CircuitPython dependencies:
```bash
pip install circup
```

If circup is installed but not found, specify the path:
```bash
# Command line
circremote -c /usr/local/bin/circup /dev/ttyUSB0 BME280

# Config file
```

Add to `~/.circremote/config.json`:
```json
{
  "circup": "/usr/local/bin/circup"
}
```

Common circup locations:
- `/usr/local/bin/circup` (pip install)
- `/opt/homebrew/bin/circup` (Homebrew on macOS)
- `~/venv/bin/circup` (virtual environment)
- `circup` (system PATH)

### Device not responding
1. Check the connection (serial port or IP address)
2. Try pressing the reset button on the device
3. Verify the device is running CircuitPython
4. Check if the device is in bootloader mode (some boards have a boot button)

### WebSocket connection timeout
1. Check if the device is running CircuitPython Web Workflow
2. Verify the IP address and port
3. Check your network connection
4. Try restarting the device

## Advanced Usage

### How do I run commands with different timeouts?
```bash
# Wait 5 seconds for output
circremote -t 5 /dev/ttyUSB0 BME280

# Wait indefinitely (until you press Ctrl+C)
circremote -t 0 /dev/ttyUSB0 BME280
```

### How do I use "double exit" mode?
Use "double exit mode" to send an extra ^D to the device in order to re-start the program in `code.py`:
```bash
circremote -d /dev/ttyUSB0 BME280
```

### How do I skip confirmation prompts?
```bash
circremote -y /dev/ttyUSB0 untested_command
```

### How do I see what's happening internally?
If something goes wrong and you want detailed debugging info, use the `-v` or `--verbose` flag.
```bash
circremote -v /dev/ttyUSB0 BME280
```

## Configuration File Security

### Why do I get a warning about file permissions?
If your config file has world-readable permissions, you'll see a warning. Fix it:
```bash
chmod 600 ~/.circremote/config.json
```

### What should I include in my config file?
```json
{
  "devices": [
    {
      "name": "my-device",
      "device": "/dev/ttyUSB0",
      "friendly_name": "My CircuitPython Device"
    }
  ],
  "command_aliases": [
    {
      "name": "temp",
      "command": "BME280"
    }
  ],
  "search_paths": [
    "~/my_commands",
    "/opt/custom_sensors"
  ],
  "circup": "/usr/local/bin/circup"
}
```

## Getting Help

### How do I see all available commands?
```bash
circremote -l
```

This lists all commands from:
- Built-in commands
- Search path commands
- User commands directory
- Command aliases (if configured)

### How do I get help for a specific command?
```bash
# Show detailed help for a command
circremote -h BME280
circremote -h clean
circremote -h ./my_custom_command

# This shows:
# - Command description
# - File location
# - Command line format
# - All arguments (required/optional)
# - Default values
# - Usage examples
```

### How do I see debug information?
```bash
circremote -v /dev/ttyUSB0 BME280
```

### How do I list all available commands?
```bash
circremote -l
```

This shows:
- **Built-in commands:** Commands that come with circremote
- **Search path commands:** Commands from your configured search paths
- **Command aliases:** Short names you've configured for commands
- **Total count:** Number of commands available

Example output:
```
Available commands:
==================================================

Built-in commands:
  BME280
  SHT30
  VL53L0X
  ...

Search path commands:
  my_custom_sensor
  ...

Command aliases:
  temp -> BME280
  light -> TSL2591

Total: 90 commands available

Use 'circremote -h COMMAND' for detailed help on any command
```

### What information does command help show?
When you run `circremote -h COMMAND`, you'll see:

**Location:** Where the command files are stored on your system
**Description:** What the command does
**Command line format:** How to use the command with positional arguments (if defined)
**Arguments:** All variables the command accepts:
- `(REQUIRED)` - Must be provided
- `(optional)` - Can use default value
- Default values are shown when available
**Examples:** Different ways to use the command

Example output:
```
Help for command: BME280
==========================

Location:
  /path/to/circremote/commands/BME280

Description:
  BME280 is a digital sensor that measures temperature, humidity, and barometric pressure...

Command line format:
  circremote <device> BME280 [variable=value ...]

Arguments:
  sda (optional)
    I2C SDA pin
    Default: board.SDA

  scl (optional)
    I2C SCL pin
    Default: board.SCL

Examples:
  circremote /dev/ttyUSB0 BME280 sda=board.IO1 scl=board.IO2
  circremote /dev/ttyUSB0 BME280
```

### Where can I find more examples?
- Check the built-in commands in the `circremote/commands/` directory
- Look at the project documentation
- Check the GitHub repository for examples

### How do I report bugs or request features?
- Open an issue on the GitHub repository
- Include the circremote version, your operating system, and steps to reproduce
- Use the `-v` flag and include the debug output 

### How do I check the circremote version?
```bash
circremote --version
# or
circremote -V
```
This will print the installed version of circremote and exit. 
