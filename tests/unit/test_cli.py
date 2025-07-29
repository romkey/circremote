"""
Unit tests for the CLI class.
"""

import pytest
import sys
from unittest.mock import Mock, patch, mock_open
from argparse import Namespace
import json

from circremote.cli import CLI


class TestCLI:
    """Test the CLI class methods."""

    def test_parse_command_line_variables(self, cli_instance):
        """Test parsing explicit variable assignments."""
        args = ['sda=board.IO1', 'scl=board.IO2', 'address=0x76']
        result = cli_instance.parse_command_line_variables(args)
        
        expected = {
            'sda': 'board.IO1',
            'scl': 'board.IO2', 
            'address': '0x76'
        }
        assert result == expected

    def test_parse_command_line_variables_with_quotes(self, cli_instance):
        """Test parsing variables with quoted values."""
        args = ['sda="board.IO1"', "scl='board.IO2'"]
        result = cli_instance.parse_command_line_variables(args)
        
        expected = {
            'sda': 'board.IO1',
            'scl': 'board.IO2'
        }
        assert result == expected

    def test_parse_command_line_variables_no_equals(self, cli_instance):
        """Test parsing arguments without equals signs."""
        args = ['not_a_variable', 'another_arg']
        result = cli_instance.parse_command_line_variables(args)
        
        assert result == {}

    def test_parse_default_commandline_variables(self, cli_instance, sample_info_json):
        """Test parsing positional arguments as variables."""
        args = ['board.IO1', 'board.IO2']
        result = cli_instance.parse_default_commandline_variables(args, sample_info_json, 'test')
        
        expected = {
            'sda': 'board.IO1',
            'scl': 'board.IO2'
        }
        assert result == expected

    def test_parse_default_commandline_variables_no_default(self, cli_instance):
        """Test parsing when no default_commandline is defined."""
        args = ['arg1', 'arg2']
        result = cli_instance.parse_default_commandline_variables(args, {}, 'test')
        
        assert result == {}

    def test_parse_default_commandline_variables_too_many_args(self, cli_instance, sample_info_json):
        """Test error handling for too many arguments."""
        args = ['board.IO1', 'board.IO2', 'extra_arg']
        
        with pytest.raises(SystemExit):
            cli_instance.parse_default_commandline_variables(args, sample_info_json, 'test')

    def test_parse_default_commandline_variables_not_enough_args(self, cli_instance, sample_info_json):
        """Test error handling for not enough arguments."""
        args = ['board.IO1']  # Missing scl
        
        with pytest.raises(SystemExit):
            cli_instance.parse_default_commandline_variables(args, sample_info_json, 'test')

    def test_validate_variables_valid(self, cli_instance, sample_info_json):
        """Test validation of valid variables."""
        variables = {'sda': 'board.IO1', 'scl': 'board.IO2'}
        
        # Should not raise an exception
        cli_instance.validate_variables(variables, sample_info_json, 'test')

    def test_validate_variables_invalid(self, cli_instance, sample_info_json):
        """Test validation of invalid variables."""
        variables = {'sda': 'board.IO1', 'invalid_var': 'value'}
        
        with pytest.raises(SystemExit):
            cli_instance.validate_variables(variables, sample_info_json, 'test')

    def test_validate_variables_no_info(self, cli_instance):
        """Test validation when no info.json is provided."""
        variables = {'sda': 'board.IO1'}
        
        # Should not raise an exception
        cli_instance.validate_variables(variables, None, 'test')

    def test_add_defaults_from_info(self, cli_instance, sample_info_json):
        """Test adding default values from info.json."""
        variables = {'sda': 'board.IO3'}  # Override default
        result = cli_instance.add_defaults_from_info(variables, sample_info_json, 'test')
        
        expected = {
            'sda': 'board.IO3',  # Should keep provided value
            'scl': 'board.IO2'   # Should add default
        }
        assert result == expected

    def test_add_defaults_from_info_no_defaults(self, cli_instance):
        """Test adding defaults when none are defined."""
        variables = {'sda': 'board.IO1'}
        info_data = {
            'variables': [
                {'name': 'sda', 'description': 'SDA pin'},
                {'name': 'scl', 'description': 'SCL pin'}  # No default
            ]
        }
        
        result = cli_instance.add_defaults_from_info(variables, info_data, 'test')
        
        expected = {'sda': 'board.IO1'}  # Should only keep provided value
        assert result == expected

    def test_interpolate_variables(self, cli_instance, sample_info_json):
        """Test variable interpolation in template content."""
        content = "import {{sda}}\nimport {{scl}}"
        variables = {'sda': 'board.IO1', 'scl': 'board.IO2'}
        
        result = cli_instance.interpolate_variables(content, variables, sample_info_json, 'test')
        
        expected = "import board.IO1\nimport board.IO2"
        assert result == expected

    def test_interpolate_variables_missing_var(self, cli_instance, sample_info_json):
        """Test error handling for missing variables."""
        content = "import {{sda}}\nimport {{missing_var}}"
        variables = {'sda': 'board.IO1'}
        
        with pytest.raises(SystemExit):
            cli_instance.interpolate_variables(content, variables, sample_info_json, 'test')

    def test_interpolate_variables_invalid_template_var(self, cli_instance, sample_info_json):
        """Test error handling for template variables not in info.json."""
        content = "import {{invalid_var}}"
        variables = {'invalid_var': 'value'}
        
        with pytest.raises(SystemExit):
            cli_instance.interpolate_variables(content, variables, sample_info_json, 'test')

    def test_looks_like_url(self, cli_instance):
        """Test URL detection."""
        assert cli_instance.looks_like_url('https://example.com/code.py')
        assert cli_instance.looks_like_url('http://github.com/user/repo/blob/main/code.py')
        assert cli_instance.looks_like_url('ftp://example.com/file.py')
        assert not cli_instance.looks_like_url('BME280')
        assert not cli_instance.looks_like_url('simple')

    def test_convert_github_url_to_raw(self, cli_instance):
        """Test GitHub URL conversion to raw content."""
        github_url = 'https://github.com/user/repo/blob/main/code.py'
        expected = 'https://raw.githubusercontent.com/user/repo/main/code.py'
        
        result = cli_instance.convert_github_url_to_raw(github_url)
        assert result == expected

    def test_convert_github_url_to_raw_tree(self, cli_instance):
        """Test GitHub tree URL conversion."""
        github_url = 'https://github.com/user/repo/tree/main/src'
        expected = 'https://raw.githubusercontent.com/user/repo/main/src'
        
        result = cli_instance.convert_github_url_to_raw(github_url)
        assert result == expected

    def test_convert_github_url_to_raw_repo_root(self, cli_instance):
        """Test GitHub repo root URL conversion."""
        github_url = 'https://github.com/user/repo'
        expected = 'https://raw.githubusercontent.com/user/repo/main/README.md'
        
        result = cli_instance.convert_github_url_to_raw(github_url)
        assert result == expected

    def test_resolve_device_from_config(self, cli_instance, mock_config):
        """Test device resolution from config."""
        cli_instance.config = mock_config
        mock_config.find_device.return_value = {
            'name': 'test-device',
            'device': '/dev/ttyUSB0',
            'password': 'testpass'
        }
        
        result = cli_instance.resolve_device('test-device', Mock())
        
        expected = {
            'name': 'test-device',
            'device': '/dev/ttyUSB0',
            'password': 'testpass'
        }
        assert result == expected

    def test_resolve_device_direct(self, cli_instance, mock_config):
        """Test direct device specification."""
        cli_instance.config = mock_config
        mock_config.find_device.return_value = None
        
        result = cli_instance.resolve_device('/dev/ttyUSB0', Mock())
        
        expected = {
            'name': '/dev/ttyUSB0',
            'device': '/dev/ttyUSB0'
        }
        assert result == expected

    def test_debug_message_verbose(self, cli_instance):
        """Test debug message output in verbose mode."""
        options = Namespace(verbose=True)
        
        with patch('builtins.print') as mock_print:
            cli_instance.debug("Test message", options)
            mock_print.assert_called_once_with("Test message")

    def test_debug_message_not_verbose(self, cli_instance):
        """Test debug message suppression when not verbose."""
        options = Namespace(verbose=False)
        
        with patch('builtins.print') as mock_print:
            cli_instance.debug("Test message", options)
            mock_print.assert_not_called()

    def test_debug_message_no_options(self, cli_instance):
        """Test debug message handling with no options."""
        with patch('builtins.print') as mock_print:
            cli_instance.debug("Test message", None)
            mock_print.assert_not_called()

    def test_parse_options_with_timeout(self, cli_instance):
        """Test parsing options with timeout."""
        args = ['-t', '30', '/dev/ttyUSB0', 'BME280']
        options, remaining = cli_instance.parse_options(args)
        
        assert options.timeout == 30.0
        assert remaining == ['/dev/ttyUSB0', 'BME280']

    def test_parse_options_with_timeout_zero(self, cli_instance):
        """Test parsing options with timeout set to zero."""
        args = ['-t', '0', '/dev/ttyUSB0', 'BME280']
        options, remaining = cli_instance.parse_options(args)
        
        assert options.timeout == 0.0
        assert remaining == ['/dev/ttyUSB0', 'BME280']

    def test_parse_options_with_timeout_float(self, cli_instance):
        """Test parsing options with fractional timeout."""
        args = ['-t', '5.5', '/dev/ttyUSB0', 'BME280']
        options, remaining = cli_instance.parse_options(args)
        
        assert options.timeout == 5.5
        assert remaining == ['/dev/ttyUSB0', 'BME280']

    def test_parse_options_with_timeout_default(self, cli_instance):
        """Test parsing options without timeout (should use default)."""
        args = ['/dev/ttyUSB0', 'BME280']
        options, remaining = cli_instance.parse_options(args)
        
        assert options.timeout == 10.0  # Default value
        assert remaining == ['/dev/ttyUSB0', 'BME280']

    def test_parse_options_with_timeout_long_form(self, cli_instance):
        """Test parsing options with long form timeout."""
        args = ['--timeout', '15', '/dev/ttyUSB0', 'BME280']
        options, remaining = cli_instance.parse_options(args)
        
        assert options.timeout == 15.0
        assert remaining == ['/dev/ttyUSB0', 'BME280']

    def test_parse_options_with_invalid_timeout(self, cli_instance):
        """Test parsing options with invalid timeout value."""
        args = ['-t', 'invalid', '/dev/ttyUSB0', 'BME280']
        
        with pytest.raises(SystemExit):
            cli_instance.parse_options(args)

    def test_parse_options_with_negative_timeout(self, cli_instance):
        """Test parsing negative timeout value."""
        args = ['--timeout', '-5']
        
        # Should accept negative values (though they may not make sense)
        options, remaining = cli_instance.parse_options(args)
        assert options.timeout == -5.0

    def test_resolve_command_path_python_file(self, cli_instance, tmp_path):
        """Test resolving a Python file pathname."""
        # Create a test Python file
        test_file = tmp_path / "test_sensor.py"
        test_file.write_text("# Test sensor code\nprint('Hello')")
        
        options = Namespace(verbose=True, skip_circup=True)
        result = cli_instance.resolve_command_path(str(test_file), options)
        
        file_content, command_dir, code_file, info_data, is_pathname = result
        assert file_content == "# Test sensor code\nprint('Hello')"
        assert command_dir is None
        assert code_file is None
        assert info_data is None
        assert is_pathname is True

    def test_resolve_command_path_directory(self, cli_instance, tmp_path):
        """Test resolving a directory pathname."""
        # Create a test directory with code.py and info.json
        test_dir = tmp_path / "test_sensor"
        test_dir.mkdir()
        
        code_file = test_dir / "code.py"
        code_file.write_text("# Test sensor code\nprint('Hello')")
        
        info_file = test_dir / "info.json"
        info_file.write_text('{"name": "Test Sensor", "description": "Test"}')
        
        options = Namespace(verbose=True, skip_circup=True)
        result = cli_instance.resolve_command_path(str(test_dir), options)
        
        file_content, command_dir, code_file, info_data, is_pathname = result
        assert file_content is None
        assert command_dir == test_dir
        assert code_file == test_dir / "code.py"
        assert info_data == {"name": "Test Sensor", "description": "Test"}
        assert is_pathname is True

    def test_resolve_command_path_directory_no_code_py(self, cli_instance, tmp_path):
        """Test resolving a directory pathname without code.py."""
        # Create a test directory without code.py
        test_dir = tmp_path / "test_sensor"
        test_dir.mkdir()
        
        options = Namespace(verbose=True, skip_circup=True)
        
        with pytest.raises(SystemExit):
            cli_instance.resolve_command_path(str(test_dir), options)

    def test_resolve_command_path_nonexistent(self, cli_instance):
        """Test resolving a nonexistent pathname."""
        options = Namespace(verbose=True, skip_circup=True)
        
        with pytest.raises(SystemExit):
            cli_instance.resolve_command_path("/nonexistent/path", options)

    def test_resolve_command_path_builtin_command(self, cli_instance):
        """Test resolving a built-in command (not a pathname)."""
        options = Namespace(verbose=True, skip_circup=True)
        result = cli_instance.resolve_command_path("BME280", options)
        
        file_content, command_dir, code_file, info_data, is_pathname = result
        assert file_content is None
        assert command_dir is None
        assert code_file is None
        assert info_data is None
        assert is_pathname is False

    def test_resolve_command_path_relative_path(self, cli_instance, tmp_path):
        """Test resolving a relative path."""
        # Create a test Python file
        test_file = tmp_path / "test_sensor.py"
        test_file.write_text("# Test sensor code\nprint('Hello')")
        
        # Change to the temp directory to test relative path
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            options = Namespace(verbose=True, skip_circup=True)
            result = cli_instance.resolve_command_path("./test_sensor.py", options)
            
            file_content, command_dir, code_file, info_data, is_pathname = result
            assert file_content == "# Test sensor code\nprint('Hello')"
            assert is_pathname is True
        finally:
            os.chdir(original_cwd)

    def test_resolve_command_path_directory_with_requirements(self, cli_instance, tmp_path):
        """Test resolving a directory pathname with requirements.txt."""
        # Create a test directory with all files
        test_dir = tmp_path / "test_sensor"
        test_dir.mkdir()
        
        code_file = test_dir / "code.py"
        code_file.write_text("# Test sensor code\nprint('Hello')")
        
        info_file = test_dir / "info.json"
        info_file.write_text('{"name": "Test Sensor"}')
        
        requirements_file = test_dir / "requirements.txt"
        requirements_file.write_text("adafruit-circuitpython-bme280")
        
        options = Namespace(verbose=True, skip_circup=False)
        result = cli_instance.resolve_command_path(str(test_dir), options)
        
        file_content, command_dir, code_file, info_data, is_pathname = result
        assert file_content is None
        assert command_dir == test_dir
        assert code_file == test_dir / "code.py"
        assert info_data == {"name": "Test Sensor"}
        assert is_pathname is True

    def test_resolve_command_path_directory_with_empty_requirements(self, cli_instance, tmp_path):
        """Test resolving a directory pathname with empty requirements.txt."""
        # Create a test directory with empty requirements.txt
        test_dir = tmp_path / "test_sensor"
        test_dir.mkdir()
        
        code_file = test_dir / "code.py"
        code_file.write_text("# Test sensor code\nprint('Hello')")
        
        requirements_file = test_dir / "requirements.txt"
        requirements_file.write_text("# Empty requirements\n\n")
        
        options = Namespace(verbose=True, skip_circup=False)
        result = cli_instance.resolve_command_path(str(test_dir), options)
        
        file_content, command_dir, code_file, info_data, is_pathname = result
        assert file_content is None
        assert command_dir == test_dir
        assert code_file == test_dir / "code.py"
        assert info_data is None
        assert is_pathname is True

    def test_find_command_in_search_paths(self, cli_instance, tmp_path):
        """Test finding commands in search paths."""
        # Create a test command in a search path
        search_path = tmp_path / 'test_commands'
        search_path.mkdir()
        command_dir = search_path / 'test_sensor'
        command_dir.mkdir()
        code_file = command_dir / 'code.py'
        code_file.write_text('# Test sensor code')
        
        # Mock config to return the search path
        cli_instance.config.search_paths = [str(search_path)]
        
        # Should find the command
        result = cli_instance.config.find_command_in_search_paths('test_sensor')
        assert result == command_dir
        
        # Should not find non-existent command
        result = cli_instance.config.find_command_in_search_paths('nonexistent')
        assert result is None

    def test_find_command_in_user_commands(self, cli_instance, tmp_path):
        """Test finding commands in user commands directory."""
        # Create a test command in user commands directory
        user_commands_dir = tmp_path / '.circremote' / 'commands'
        user_commands_dir.mkdir(parents=True)
        command_dir = user_commands_dir / 'test_sensor'
        command_dir.mkdir()
        code_file = command_dir / 'code.py'
        code_file.write_text('# Test sensor code')
        
        with patch('pathlib.Path.home', return_value=tmp_path):
            # Should find the command
            result = cli_instance.config.find_command_in_search_paths('test_sensor')
            assert result == command_dir

    def test_search_paths_warning_for_nonexistent(self, cli_instance, tmp_path, capsys):
        """Test warning for nonexistent search paths."""
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
            # Create new config instance to trigger loading
            from circremote.config import Config
            config = Config()
            captured = capsys.readouterr()
            
            # Should show warnings for nonexistent paths
            assert 'Warning: Search path' in captured.out
            assert '/nonexistent/path1' in captured.out
            assert '/another/nonexistent/path' in captured.out
            
            # Should have no search paths
            assert config.search_paths == []

    def test_parse_options_with_circup_path(self, cli_instance):
        """Test parsing -u option for circup path."""
        args = ['-u', '/usr/local/bin/circup', '/dev/ttyUSB0', 'BME280']
        options, remaining = cli_instance.parse_options(args)
        
        assert options.circup == '/usr/local/bin/circup'
        assert remaining == ['/dev/ttyUSB0', 'BME280']

    def test_parse_options_with_circup_path_long_form(self, cli_instance):
        """Test parsing --circup option for circup path."""
        args = ['--circup', '/opt/homebrew/bin/circup', '/dev/ttyUSB0', 'BME280']
        options, remaining = cli_instance.parse_options(args)
        
        assert options.circup == '/opt/homebrew/bin/circup'
        assert remaining == ['/dev/ttyUSB0', 'BME280']

    def test_parse_options_with_circup_and_other_options(self, cli_instance):
        """Test parsing -u option with other options."""
        args = ['-v', '-u', '/usr/local/bin/circup', '-c', '/dev/ttyUSB0', 'BME280']
        options, remaining = cli_instance.parse_options(args)
        
        assert options.verbose is True
        assert options.circup == '/usr/local/bin/circup'
        assert options.skip_circup is True
        assert remaining == ['/dev/ttyUSB0', 'BME280']

    def test_show_command_help_builtin_command(self, cli_instance, tmp_path):
        """Test showing help for a built-in command."""
        # Create a mock BME280 command directory
        commands_dir = tmp_path / 'commands'
        commands_dir.mkdir()
        bme280_dir = commands_dir / 'BME280'
        bme280_dir.mkdir()
        
        info_file = bme280_dir / 'info.json'
        info_data = {
            'description': 'BME280 temperature sensor',
            'variables': [
                {
                    'name': 'sda',
                    'description': 'I2C SDA pin',
                    'default': 'board.SDA'
                }
            ]
        }
        info_file.write_text(json.dumps(info_data))
        
        # Mock the resolve_command_path method to return our test data
        with patch.object(cli_instance, 'resolve_command_path') as mock_resolve:
            mock_resolve.return_value = (None, bme280_dir, bme280_dir / 'code.py', info_data, False)
            
            # Test that the method runs without error
            options = Namespace(skip_circup=False, verbose=False)
            cli_instance.show_command_help('BME280', options)

    def test_show_command_help_nonexistent_command(self, cli_instance, capsys):
        """Test showing help for a nonexistent command."""
        cli_instance.show_command_help('nonexistent', None)
        
        # Check that error was displayed
        captured = capsys.readouterr()
        assert 'Command \'nonexistent\' not found' in captured.out

    def test_list_all_commands(self, cli_instance, tmp_path, capsys):
        """Test listing all commands."""
        # Create mock command directories
        commands_dir = tmp_path / 'commands'
        commands_dir.mkdir()
        
        # Create some built-in commands
        (commands_dir / 'BME280').mkdir()
        (commands_dir / 'BME280' / 'code.py').write_text('# BME280 code')
        (commands_dir / 'SHT30').mkdir()
        (commands_dir / 'SHT30' / 'code.py').write_text('# SHT30 code')
        
        with patch('circremote.cli.Path') as mock_path:
            # Mock the Path(__file__).parent / 'commands' call
            mock_parent = Mock()
            mock_parent.__truediv__ = Mock(return_value=commands_dir)
            mock_path.return_value.parent = mock_parent
            
            # Test that the method runs without error
            cli_instance.list_all_commands(None)
            
            # Check that some output was captured
            captured = capsys.readouterr()
            assert 'Available commands:' in captured.out

    def test_list_all_commands_with_search_paths(self, cli_instance, tmp_path):
        """Test listing commands including search paths."""
        # Create search path commands
        search_path = tmp_path / 'search_commands'
        search_path.mkdir()
        (search_path / 'custom_sensor').mkdir()
        (search_path / 'custom_sensor' / 'code.py').write_text('# Custom sensor')
        
        # Create built-in commands
        commands_dir = tmp_path / 'commands'
        commands_dir.mkdir()
        (commands_dir / 'BME280').mkdir()
        (commands_dir / 'BME280' / 'code.py').write_text('# BME280 code')
        
        # Set up config with search paths
        cli_instance.config.search_paths = [str(search_path)]
        
        with patch('circremote.cli.Path') as mock_path:
            mock_parent = Mock()
            mock_parent.__truediv__ = Mock(return_value=commands_dir)
            mock_path.return_value.parent = mock_parent
            
            # Test that the method runs without error
            cli_instance.list_all_commands(None)

    def test_list_all_commands_with_aliases(self, cli_instance, tmp_path):
        """Test listing commands including aliases."""
        # Set up config with aliases (should be a dict mapping alias name to command)
        cli_instance.config.command_aliases = {
            'temp': 'BME280',
            'light': 'TSL2591'
        }
        
        # Create built-in commands
        commands_dir = tmp_path / 'commands'
        commands_dir.mkdir()
        (commands_dir / 'BME280').mkdir()
        (commands_dir / 'BME280' / 'code.py').write_text('# BME280 code')
        
        with patch('circremote.cli.Path') as mock_path:
            mock_parent = Mock()
            mock_parent.__truediv__ = Mock(return_value=commands_dir)
            mock_path.return_value.parent = mock_parent
            
            # Test that the method runs without error
            cli_instance.list_all_commands(None)

    def test_handle_circup_installation_with_custom_path(self, cli_instance, tmp_path):
        """Test circup installation with custom path from config."""
        # Create a requirements file
        requirements_file = tmp_path / 'requirements.txt'
        requirements_file.write_text('adafruit_bme280\n')
    
        # Set up config with custom circup path
        cli_instance.config.circup_path = '/usr/local/bin/circup'
    
        # Create options object with required attributes
        from argparse import Namespace
        options = Namespace(yes=False, verbose=False)
    
        with patch('os.path.exists', return_value=True), \
             patch('os.access', return_value=True), \
             patch('builtins.print') as mock_print, \
             patch('builtins.input', return_value='s'):  # Mock input to return 'skip'
    
            cli_instance.handle_circup_installation(requirements_file, '/dev/ttyUSB0', None, options)
            
            # Check that print was called (indicating the method ran)
            mock_print.assert_called()

    def test_handle_circup_installation_with_command_line_path(self, cli_instance, tmp_path):
        """Test circup installation with command line path."""
        # Create a requirements file
        requirements_file = tmp_path / 'requirements.txt'
        requirements_file.write_text('adafruit_bme280\n')
        
        # Set up config with custom circup path
        cli_instance.config.circup_path = '/opt/homebrew/bin/circup'
        
        # Set up options with command line path and required attributes
        from argparse import Namespace
        options = Namespace(circup='/usr/local/bin/circup', yes=False, verbose=False)
        cli_instance.config.options = options
        
        with patch('os.path.exists', return_value=True), \
             patch('os.access', return_value=True), \
             patch('builtins.print') as mock_print, \
             patch('builtins.input', return_value='s'):  # Mock input to return 'skip'
            
            cli_instance.handle_circup_installation(requirements_file, '/dev/ttyUSB0', None, options)
            
            # Check that print was called (indicating the method ran)
            mock_print.assert_called()

    def test_handle_circup_installation_path_not_found(self, cli_instance, tmp_path):
        """Test circup installation when specified path is not found."""
        # Create a requirements file
        requirements_file = tmp_path / 'requirements.txt'
        requirements_file.write_text('adafruit_bme280\n')
        
        # Set up config with custom circup path
        cli_instance.config.circup_path = '/nonexistent/circup'
        
        # Create options object with required attributes
        from argparse import Namespace
        options = Namespace(yes=False, verbose=False)
        
        with patch('os.path.exists', return_value=False), \
             patch('builtins.print') as mock_print:
            
            cli_instance.handle_circup_installation(requirements_file, '/dev/ttyUSB0', None, options)
            
            # Check that error was displayed
            mock_print.assert_called() 

    def test_version_option(self, cli_instance):
        """Test that --version and -V print the version and exit."""
        from circremote.version import VERSION
        import builtins
        import io
        from unittest.mock import patch
        
        # Test --version
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            with pytest.raises(SystemExit):
                cli_instance.run(["--version"])
            output = mock_stdout.getvalue()
            assert f"circremote version {VERSION}" in output
        
        # Test -V
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            with pytest.raises(SystemExit):
                cli_instance.run(["-V"])
            output = mock_stdout.getvalue()
            assert f"circremote version {VERSION}" in output

    def test_parse_options_with_config_file(self, cli_instance):
        """Test the -C/--config option."""
        options, remaining = cli_instance.parse_options(['-C', '/path/to/config.json'])
        assert options.config == '/path/to/config.json'
        assert remaining == []

    def test_parse_options_with_config_file_long_form(self, cli_instance):
        """Test the --config option."""
        options, remaining = cli_instance.parse_options(['--config', '/path/to/config.json'])
        assert options.config == '/path/to/config.json'
        assert remaining == []

    def test_parse_options_with_config_and_other_options(self, cli_instance):
        """Test config option with other options."""
        options, remaining = cli_instance.parse_options([
            '-C', '/path/to/config.json',
            '-v',
            '-u', '/usr/local/bin/circup',
            '/dev/ttyUSB0', 'BME280'
        ])
        assert options.config == '/path/to/config.json'
        assert options.verbose is True
        assert options.circup == '/usr/local/bin/circup'
        assert remaining == ['/dev/ttyUSB0', 'BME280']

    def test_cli_uses_custom_config_file(self, cli_instance, tmp_path):
        """Test that CLI uses custom config file when specified."""
        # Create a custom config file
        config_file = tmp_path / 'custom_config.json'
        config_data = {
            'devices': [
                {
                    'name': 'test_device',
                    'device': '/dev/ttyUSB0',
                    'friendly_name': 'Test Device'
                }
            ]
        }
        config_file.write_text(json.dumps(config_data))
        
        # Test that the config path is set correctly when options are passed
        from argparse import Namespace
        options = Namespace(config=str(config_file), verbose=False)
        
        # Create a new Config instance with the options
        from circremote.config import Config
        config = Config(options)
        
        # Verify the config path is set to our custom file
        assert config.config_path == config_file 