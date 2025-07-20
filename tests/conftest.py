"""
Pytest configuration and common fixtures for circremote-python tests.
"""

import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch
from argparse import Namespace

from circremote.cli import CLI
from circremote.config import Config
from circremote.connection import CircuitPythonConnection


@pytest.fixture
def commands_dir():
    """Return the path to the commands directory."""
    return Path(__file__).parent.parent / 'circremote' / 'commands'


@pytest.fixture
def sample_command_dir(commands_dir):
    """Return the path to a sample command directory (BME280)."""
    return commands_dir / 'BME280'


@pytest.fixture
def sample_info_json():
    """Return sample info.json data."""
    return {
        "description": "BME280 temperature, humidity, and pressure sensor",
        "variables": [
            {
                "name": "sda",
                "description": "I2C SDA pin",
                "default": "board.IO1"
            },
            {
                "name": "scl", 
                "description": "I2C SCL pin",
                "default": "board.IO2"
            }
        ],
        "default_commandline": "sda scl"
    }


@pytest.fixture
def sample_code_py():
    """Return sample code.py content."""
    return '''# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import adafruit_bme280.advanced as adafruit_bme280

# Initialize I2C
i2c = board.I2C()

# Initialize BME280
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

# Main reading loop
while True:
    print(f"Temperature: {bme280.temperature:.1f}°C")
    print(f"Humidity: {bme280.relative_humidity:.1f}%")
    print(f"Pressure: {bme280.pressure:.1f} hPa")
    print("-" * 30)
    time.sleep(30)
'''


@pytest.fixture
def cli_instance():
    """Return a CLI instance for testing."""
    options = Namespace(verbose=False, password=None, double_exit=False, 
                       skip_circup=False, yes=False)
    return CLI(options)


@pytest.fixture
def mock_serial_connection():
    """Mock serial connection for testing."""
    mock_conn = Mock(spec=CircuitPythonConnection)
    mock_conn.connection_type = 'serial'
    mock_conn.write = Mock()
    mock_conn.read_nonblock = Mock(return_value="***START***\nTest output\n***END***\n")
    mock_conn.flush = Mock()
    mock_conn.close = Mock()
    return mock_conn


@pytest.fixture
def mock_websocket_connection():
    """Mock WebSocket connection for testing."""
    mock_conn = Mock(spec=CircuitPythonConnection)
    mock_conn.connection_type = 'websocket'
    mock_conn.write = Mock()
    mock_conn.on_message = Mock()
    mock_conn.flush = Mock()
    mock_conn.close = Mock()
    return mock_conn


@pytest.fixture
def temp_command_dir():
    """Create a temporary command directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        yield temp_path


@pytest.fixture
def sample_command_files(temp_command_dir, sample_info_json, sample_code_py):
    """Create sample command files in a temporary directory."""
    # Create info.json
    info_file = temp_command_dir / 'info.json'
    with open(info_file, 'w') as f:
        json.dump(sample_info_json, f, indent=2)
    
    # Create code.py
    code_file = temp_command_dir / 'code.py'
    with open(code_file, 'w') as f:
        f.write(sample_code_py)
    
    # Create requirements.txt
    req_file = temp_command_dir / 'requirements.txt'
    with open(req_file, 'w') as f:
        f.write('adafruit-circuitpython-bme280\n')
    
    return temp_command_dir


@pytest.fixture
def mock_config():
    """Mock config for testing."""
    config = Mock(spec=Config)
    config.find_device.return_value = None
    config.find_command_alias.return_value = None
    return config 