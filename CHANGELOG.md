# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
