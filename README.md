# `circremote`

A command-line tool for uploading and running Python code on CircuitPython devices via serial or Web Workflow websocket connections, with support for dependency management and sensor libraries.

A few examples:
```
# simple I2C scanner on locally connected device
circremote /dev/ttyUSB0 scan-i2c

# show the contents of settings.toml on a Web Workflow device
circremote 192.168.1.23:8080 -p PASSWORD cat settings.toml

# run Adafruit's I2C scanner on a device with the nickname feather-s3
circremote feather-s3 https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/main/I2C_Scanners/circuitpython/code.py

# help
circremote -h
```

## Overview

`circremote` is a utility program that allows you to easily upload and run code on a CircuitPython device without disturbing code.py.

It works with devices connected over USB and over a network connection to devices that support and are configured for the Web Workflow.

It includes a library of small programs ("commands") which perform utility functions like scanning the I2C bus or cleaning up undesired files from the internal flash filesystem, as well as example programs that work with a variety of sensors and other devices.

It can run the commands included with it, your own commands from anywhere in the filesystem, and commands that it loads over HTTP/HTTPS. It can easily execute example programs from Github.

Commands can include a `requirements.txt` file and `circup` will automatically be run to install them. Commands can also take arguments, so you can (for instance) pass the I2C SDA and SCL pins to a command, or specify the address of a sensor.

For your convenience you can also configure aliases for devices and commands.
It can also pull code from a web server, so you can run Adafruit example code directly from Github if you want.

It does not currently support Microsoft Windows. I do not have a Windows machine and have no way to test it with Windows. I understand that a lot of people use Windows and that the lack of support means that a lot of people who might benefit from `circremote` won't be able to use it. While I'm happy to spend some time and resources on continuing to develop `circremote` and support users, I don't have the time, energy or desire to bring up a new platform and get it working on it. If a motivated co-maintainer comes along who'd like to get `circremote` working properly with Windows and then support it, I'd be happy to bring someone like that onto the project.

- [About `circremote`](doc/about.md)
- [Install](doc/install.md)
- [Usage](doc/usage.md)
- [Commands](doc/commands.md)
- [Configuration](doc/configuration.md)
- [Contributing](doc/contributing.md)
- [Development](doc/development.md)
- [Testing](doc/testing.md)
- [Release](doc/release.md)
- [FAQ](doc/faq.md)

## Rough Edges

There are still some rough edges in dealing with program termination and resuming `code.py` (the "double exit" mode). Programs can continue running indefinitely, which may or may not be desired. Many commands are untested because I either don't have the hardware or haven't had the time to get to them.

## Getting Help

If you run into problems, first - if you're using Microsoft Windows, this is currently unsupported and we cannot help you.

Please review the [FAQ](doc/faq.md).

If you're unable to resolve the problem with `circremote` file an issue here on Github.

General CircuitPython help is available at [#help-with-circuitpython on Adafruit's Discord server[(https://discord.com/channels/327254708534116352/537365702651150357) and at [r/circuitpython](https://www.reddit.com/r/circuitpython/) on Reddit.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- CircuitPython community for the excellent ecosystem
- Adafruit for the sensor libraries
- Python community for, well... Python
