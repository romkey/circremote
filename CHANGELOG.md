# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

New commands (all untested):
- ADS7128
- APDS9999
- AS7343
- ENS161
- GP8403
- MAX44009
- OPT4048
- SCD43
- SGP41
- STHS34PF80
- TCS3430
- TMAG5273A1
- TMAG5273A2
- TMP119
- VCNL4030

Documentation:
- Added Read the Docs support. The Markdown in `doc/` is now built with
  MkDocs and published at https://circremote.readthedocs.io/.

Fixed:
- Reliably enter raw REPL mode before uploading code. The REPL handshake now
  reads and verifies the device's responses (the `>>>` prompt, the raw REPL
  banner, and the `OK` execution acknowledgment) instead of using fixed
  delays, retrying each step as needed. Previously, the first run against a
  device that was still executing code.py (common with Web Workflow
  connections) could paste the program into the normal REPL, where
  auto-indent mangled it.

## [0.13.1] - 2025-09-21

New commands:
- STCC4
- analog-read
- benchmark
- ble-scan
- digital-read
- digital-write
- gps-serial
- matrix-diagnostic
- matrix-rainbow
- onewire
- pwm-write
- stop

## [0.12.1] - 2025-09-12

Tested and fixed commands:
- ADXL343
- BMP280 
- DS18B20
- DS248x (formerly DS2484) 
- LTR-329
- MLX90393 
- MMC5603
- Si7021 
- TLV493D 
- VEML7700
- neopixel-rainbow

## [0.12.0] - 2025-08-14

Windows support! Mostly worked on Windows already but this update
makes timeouts work properly, runs `circup` under Windows,  properly
locates the `config.json` file and updates the documentation.

New `enable-webworkflow` and `erase_fs` commands

Tested more commands (mostly light sensors), added VEML6075 UV sensor,
VCNL4040 proximity sensor, and combined BMP3XX sensors into one command.

### Added
- Global variable defaults support via `variable_defaults` in config.json
- Enhanced variable resolution priority: command line > device defaults > global defaults > command defaults

## [0.11.0] - 2025-08-11

Added "quiet mode" -q to eliminate noise, for use in testing environments.

Also new `ls` and `rm` commands to list and remove files.

## [0.10.2] - 2025-08-07

Fixed package building to properly omit files and use pypackage.toml
and MANFEST.in and not setuptools.py

No functional changes, only packaging.

## [0.10.0] - 2025-08-07 

### Added
- Initial release with core functionality
- Support for serial and WebSocket connections
- Built-in command library for sensors and utilities
- Configuration system with device aliases
- Dependency management with circup integration
- Support for local and remote command execution

### Features
- Upload and run Python code on CircuitPython devices
- I2C bus scanning and sensor communication
- File system operations (clean, cat, etc.)
- Network utilities (ping, WiFi scanning)
- Hardware abstraction for various sensors and displays

## [0.10.1] - 2025-08-08

- PyPI support
