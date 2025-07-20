"""
Unit tests for the Config class (matches actual implementation).
"""

import pytest
import json
from pathlib import Path
from unittest.mock import patch, mock_open

from circremote.config import Config

class TestConfig:
    def test_init_sets_attributes(self):
        config = Config()
        assert hasattr(config, 'devices')
        assert hasattr(config, 'command_aliases')
        assert hasattr(config, 'config_path')

    def test_find_device_and_alias(self):
        config = Config()
        config.devices = {
            'dev1': {'name': 'dev1', 'device': '/dev/ttyUSB0'},
            'dev2': {'name': 'dev2', 'device': '/dev/ttyUSB1'}
        }
        config.command_aliases = {
            'foo': 'BME280',
            'bar': 'SHT30'
        }
        assert config.find_device('dev1') == {'name': 'dev1', 'device': '/dev/ttyUSB0'}
        assert config.find_device('dev2') == {'name': 'dev2', 'device': '/dev/ttyUSB1'}
        assert config.find_device('nope') is None
        assert config.find_command_alias('foo') == 'BME280'
        assert config.find_command_alias('bar') == 'SHT30'
        assert config.find_command_alias('nope') is None

    def test_list_devices_and_aliases(self):
        config = Config()
        config.devices = {
            'dev1': {'name': 'dev1', 'device': '/dev/ttyUSB0'},
            'dev2': {'name': 'dev2', 'device': '/dev/ttyUSB1'}
        }
        config.command_aliases = {
            'foo': 'BME280',
            'bar': 'SHT30'
        }
        assert set(config.list_devices()) == {'dev1', 'dev2'}
        assert set(config.list_command_aliases()) == {'foo', 'bar'}

    def test_load_config_file_devices_and_aliases(self, tmp_path):
        # Prepare a config file with devices and aliases
        config_data = {
            'devices': [
                {'name': 'dev1', 'device': '/dev/ttyUSB0'},
                {'name': 'dev2', 'device': '/dev/ttyUSB1'}
            ],
            'command_aliases': [
                {'name': 'foo', 'command': 'BME280'},
                {'name': 'bar', 'command': 'SHT30'}
            ]
        }
        config_dir = tmp_path / '.circremote'
        config_dir.mkdir()
        config_path = config_dir / 'config.json'
        config_path.write_text(json.dumps(config_data))
        with patch('pathlib.Path.home', return_value=tmp_path):
            config = Config()
            assert set(config.devices.keys()) == {'dev1', 'dev2'}
            assert config.devices['dev1']['device'] == '/dev/ttyUSB0'
            assert set(config.command_aliases.keys()) == {'foo', 'bar'}
            assert config.command_aliases['foo'] == 'BME280'

    def test_load_config_file_missing(self, tmp_path):
        # No config file present
        config_dir = tmp_path / '.circremote'
        config_dir.mkdir()
        with patch('pathlib.Path.home', return_value=tmp_path):
            config = Config()
            assert config.devices == {}
            assert config.command_aliases == {}

    def test_load_config_file_invalid_json(self, tmp_path):
        config_dir = tmp_path / '.circremote'
        config_dir.mkdir()
        config_path = config_dir / 'config.json'
        config_path.write_text('invalid json')
        with patch('pathlib.Path.home', return_value=tmp_path):
            with pytest.raises(SystemExit):
                Config()

    def test_validate_device_config(self):
        config = Config()
        # Valid device
        config.validate_device_config({'name': 'dev', 'device': '/dev/ttyUSB0'})
        # Missing name
        with pytest.raises(ValueError):
            config.validate_device_config({'device': '/dev/ttyUSB0'})
        # Missing device
        with pytest.raises(ValueError):
            config.validate_device_config({'name': 'dev'})
        # Wrong type
        with pytest.raises(ValueError):
            config.validate_device_config('not a dict')
        # Wrong type for friendly_name
        with pytest.raises(ValueError):
            config.validate_device_config({'name': 'dev', 'device': '/dev/ttyUSB0', 'friendly_name': 123})
        # Wrong type for password
        with pytest.raises(ValueError):
            config.validate_device_config({'name': 'dev', 'device': '/dev/ttyUSB0', 'password': 123})

    def test_validate_command_alias_config(self):
        config = Config()
        # Valid alias
        config.validate_command_alias_config({'name': 'foo', 'command': 'BME280'})
        # Missing name
        with pytest.raises(ValueError):
            config.validate_command_alias_config({'command': 'BME280'})
        # Missing command
        with pytest.raises(ValueError):
            config.validate_command_alias_config({'name': 'foo'})
        # Wrong type
        with pytest.raises(ValueError):
            config.validate_command_alias_config('not a dict') 