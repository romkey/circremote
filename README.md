# circremote

A command-line tool for uploading and running Python code on CircuitPython devices via serial or Web Workflow websocket connections, with support for dependency management and sensor libraries.

## Overview

This project maintains a set of snippets of CircuitPython code - things like an I2C scanner, a program which cleans up unwanted files left by text editors and operating systems, code for a large variety of sensors which will output the sensor's current readings, and other small programs. It can interrupt a program currently running on a CircuitPython device and transmit and execute this code over a USB serial connection. It also works with CircuitPython devices that are configured to use the "Web Workflow", which allows you to access files and run code over a small HTTP server that CircuitPython itself manages - so you can run code on a remote CircuitPython device that you're not physically connected to.

The snippets can include dependencies; each has its own `requirements.txt` file and circremote can automatically use `circup` to install those dependencies either locally to `CIRCUITPY` or over a network using the Web Workflow.

It can also pull code from a web server, so you can run Adafruit example code directly from Github if you want.

It supports a search path for code locations, so you can define your own or use other people's libraries, and fall back to the ones bundled with circremote.

circremote does not support Microsoft Windows. I do not have a Windows machine and have no way to test it with Windows. I understand that a lot of people use Windows and that the lack of support means that a lot of people who might benefit from circremote won't be able to use it. While I'm happy to spend some time and resources on continuing to develop circremote and support users, I don't have the time, energy or desire to bring up a new platform and get it working on it. If a motivated co-maintainer comes along who'd like to get circremote working properly with Windows and then support it, I'd be happy to bring someone like that onto the project.

From here, see how to install circremote and then please check out the [FAQ](doc/FAQ.md) to see how to use it.

- [About circremote](doc/about.md)
- [Install](doc/install.md)
- [Usage](doc/usage.md)
- [Commands](doc/commands.md)
- [Configuration](doc/configuration.md)
- [Contributing](doc/contributing.md)

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
