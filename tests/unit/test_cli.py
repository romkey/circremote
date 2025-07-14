"""
Unit tests for the CLI class.
"""

import pytest
import sys
from unittest.mock import Mock, patch, mock_open
from argparse import Namespace

from cpctrl.cli import CLI


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