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

    def test_validate_search_path_config(self):
        config = Config()
        # Valid search path
        config.validate_search_path_config('/path/to/commands')
        config.validate_search_path_config('~/commands')
        # Empty string
        with pytest.raises(ValueError):
            config.validate_search_path_config('')
        # Whitespace only
        with pytest.raises(ValueError):
            config.validate_search_path_config('   ')
        # Wrong type
        with pytest.raises(ValueError):
            config.validate_search_path_config(123)

    def test_load_config_file_with_search_paths(self, tmp_path):
        # Prepare a config file with search paths
        config_data = {
            'search_paths': [
                str(tmp_path / 'test_commands'),  # Use tmp_path for absolute path
                '/nonexistent/path',
                '~/custom_commands'
            ]
        }
        config_dir = tmp_path / '.circremote'
        config_dir.mkdir()
        config_path = config_dir / 'config.json'
        config_path.write_text(json.dumps(config_data))
        
        # Create one of the search paths
        test_commands_dir = tmp_path / 'test_commands'
        test_commands_dir.mkdir()
        
        with patch('pathlib.Path.home', return_value=tmp_path):
            config = Config()
            # Should only include existing paths
            assert len(config.search_paths) == 1
            # The path should be resolved to the actual path
            assert any(str(test_commands_dir) in path for path in config.search_paths)

    def test_find_command_in_search_paths(self, tmp_path):
        config = Config()
        
        # Create a test command in a search path
        search_path = tmp_path / 'test_commands'
        search_path.mkdir()
        command_dir = search_path / 'test_sensor'
        command_dir.mkdir()
        code_file = command_dir / 'code.py'
        code_file.write_text('# Test sensor code')
        
        config.search_paths = [str(search_path)]
        
        # Should find the command
        result = config.find_command_in_search_paths('test_sensor')
        assert result == command_dir
        
        # Should not find non-existent command
        result = config.find_command_in_search_paths('nonexistent')
        assert result is None

    def test_find_command_in_search_paths_no_code_py(self, tmp_path):
        config = Config()
        
        # Create a directory without code.py
        search_path = tmp_path / 'test_commands'
        search_path.mkdir()
        command_dir = search_path / 'test_sensor'
        command_dir.mkdir()
        # No code.py file
        
        config.search_paths = [str(search_path)]
        
        # Should not find the command
        result = config.find_command_in_search_paths('test_sensor')
        assert result is None

    def test_find_command_in_user_commands(self, tmp_path):
        config = Config()
        
        # Create a test command in user commands directory
        user_commands_dir = tmp_path / '.circremote' / 'commands'
        user_commands_dir.mkdir(parents=True)
        command_dir = user_commands_dir / 'test_sensor'
        command_dir.mkdir()
        code_file = command_dir / 'code.py'
        code_file.write_text('# Test sensor code')
        
        with patch('pathlib.Path.home', return_value=tmp_path):
            # Should find the command
            result = config.find_command_in_search_paths('test_sensor')
            assert result == command_dir

    def test_find_command_search_order(self, tmp_path):
        config = Config()
        
        # Create commands in multiple locations
        search_path1 = tmp_path / 'search1'
        search_path1.mkdir()
        command1_dir = search_path1 / 'test_sensor'
        command1_dir.mkdir()
        code_file1 = command1_dir / 'code.py'
        code_file1.write_text('# Search path 1 code')
        
        search_path2 = tmp_path / 'search2'
        search_path2.mkdir()
        command2_dir = search_path2 / 'test_sensor'
        command2_dir.mkdir()
        code_file2 = command2_dir / 'code.py'
        code_file2.write_text('# Search path 2 code')
        
        # Set search paths in order
        config.search_paths = [str(search_path1), str(search_path2)]
        
        # Should find the command in the first search path
        result = config.find_command_in_search_paths('test_sensor')
        assert result == command1_dir

    def test_search_paths_warning_for_nonexistent(self, tmp_path, capsys):
        # Prepare a config file with nonexistent search paths
        config_data = {
            'search_paths': [
                '/nonexistent/path1',
                '/another/nonexistent/path'
            ]
        }
        config_dir = tmp_path / '.circremote'
        config_dir.mkdir()
        config_path = config_dir / 'config.json'
        config_path.write_text(json.dumps(config_data))
        
        with patch('pathlib.Path.home', return_value=tmp_path):
            config = Config()
            captured = capsys.readouterr()
            
            # Should show warnings for nonexistent paths
            assert 'Warning: Search path' in captured.out
            assert '/nonexistent/path1' in captured.out
            assert '/another/nonexistent/path' in captured.out
            
            # Should have no search paths
            assert config.search_paths == []

    def test_load_config_file_with_circup_path(self, tmp_path):
        """Test loading config file with circup path."""
        config_data = {
            'circup': '/usr/local/bin/circup'
        }
        config_dir = tmp_path / '.circremote'
        config_dir.mkdir()
        config_path = config_dir / 'config.json'
        config_path.write_text(json.dumps(config_data))
        
        with patch('pathlib.Path.home', return_value=tmp_path):
            config = Config()
            assert config.circup_path == '/usr/local/bin/circup'

    def test_load_config_file_without_circup_path(self, tmp_path):
        """Test loading config file without circup path."""
        config_data = {
            'devices': []
        }
        config_dir = tmp_path / '.circremote'
        config_dir.mkdir()
        config_path = config_dir / 'config.json'
        config_path.write_text(json.dumps(config_data))
        
        with patch('pathlib.Path.home', return_value=tmp_path):
            config = Config()
            assert config.circup_path is None

    def test_get_circup_path_command_line_precedence(self):
        """Test that command line option takes precedence over config file."""
        from argparse import Namespace
        
        config = Config()
        config.circup_path = '/opt/homebrew/bin/circup'  # Config file setting
        options = Namespace(circup='/usr/local/bin/circup')  # Command line option
        
        config.options = options
        assert config.get_circup_path() == '/usr/local/bin/circup'

    def test_get_circup_path_config_file(self):
        """Test that config file setting is used when no command line option."""
        config = Config()
        config.circup_path = '/opt/homebrew/bin/circup'
        
        assert config.get_circup_path() == '/opt/homebrew/bin/circup'

    def test_get_circup_path_default(self):
        """Test that default 'circup' is returned when no custom path specified."""
        config = Config()
        config.circup_path = None
        
        assert config.get_circup_path() == 'circup'

    def test_get_circup_path_no_options(self):
        """Test get_circup_path when options is None."""
        config = Config()
        config.options = None
        config.circup_path = '/opt/homebrew/bin/circup'
        
        assert config.get_circup_path() == '/opt/homebrew/bin/circup'

    def test_get_circup_path_options_no_circup(self):
        """Test get_circup_path when options has no circup attribute."""
        from argparse import Namespace
        
        config = Config()
        config.circup_path = '/opt/homebrew/bin/circup'
        options = Namespace(verbose=True)  # No circup attribute
        
        config.options = options
        assert config.get_circup_path() == '/opt/homebrew/bin/circup' 