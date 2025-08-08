# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Support for remote command execution from GitHub and other web servers
- Docker containerization with circup integration
- I2C display commands (OLED, LCD, LED Matrix, TFT)
- GitHub issue templates and PR management workflows
- `--version` CLI option
- `-c` option to skip circup dependency installation
- `-C` option to specify config file path
- `-u` option to specify circup executable path

### Changed
- Renamed CLI options: `-C` (skip-circup) → `-c`, `-f` (config) → `-C`, `-c` (circup) → `-u`
- Updated info.json files: removed `warn_offline`, renamed `warn_unavailable` to `warn_offline`
- Improved error handling and graceful exits
- Enhanced Docker support with proper circup integration

### Fixed
- Pytest spewing garbage on Ctrl+C interruption
- Double circup execution for remote commands
- Docker container permission issues
- GitHub URL conversion for remote command fetching

## [0.10.0] - 2025-01-XX

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
