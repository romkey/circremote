# Configuration

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
