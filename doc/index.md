# circremote

A command-line tool for remotely executing CircuitPython code ("commands") on devices over serial or Web Workflow connections.

It can run the commands included with it, your own commands from anywhere in the filesystem, and commands that it loads over HTTP/HTTPS. It can easily execute example programs from Github.

## Features

- **Cross-platform support**: Works on Windows, macOS, and Linux
- **Multiple connection types**: Serial ports and CircuitPython Web Workflow
- **Built-in commands**: 100+ sensor and utility commands included
- **Remote commands**: Execute commands from URLs and GitHub repositories
- **Dependency management**: Automatic installation of CircuitPython libraries via circup
- **Configuration**: Device aliases and search paths for easy management
- **Quiet mode**: Suppress output for scripting and automation

## Installation

```bash
pip install circremote
```

See [Install](install.md) for other installation methods, including Docker and installing from source.

## Quick Start

```bash
# List files on a device connected over serial
circremote /dev/ttyUSB0 ls /

# Read a sensor
circremote /dev/ttyUSB0 BME280

# Get board info: CircuitPython version, memory and flash size, pin definitions
circremote /dev/ttyUSB0 info

# Scan the I2C bus
circremote /dev/ttyUSB0 scan-i2c sda=board.SDA scl=board.SCL

# Connect to a device over the network with Web Workflow
circremote -p mypassword 192.168.1.100 BME280

# Run a command straight from GitHub
circremote /dev/ttyUSB0 https://github.com/user/repo/tree/main/commands/BME280
```

## Where to next

- [Usage Guide](usage.md) - connections, options, and variables
- [Available Commands](commands.md) - the built-in sensor and utility commands
- [Configuration](configuration.md) - device aliases, search paths, and variable defaults
- [FAQ](faq.md) - common questions and troubleshooting
- [Development](development.md) - working on `circremote` itself

## License

MIT License - see the [LICENSE](https://github.com/romkey/circremote/blob/main/LICENSE) file for details.
