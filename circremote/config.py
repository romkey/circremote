# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: MIT

import json
import os
import stat
import getpass
from pathlib import Path


class Config:
    def __init__(self, options=None):
        # Use custom config file path if specified in options
        if options and hasattr(options, 'config') and options.config:
            self.config_path = Path(options.config)
        else:
            self.config_path = Path.home() / '.circremote' / 'config.json'
        
        self.devices = {}
        self.command_aliases = {}
        self.search_paths = []
        self.circup_path = None
        self.options = options
        self.load_config()

    def find_device(self, name):
        """Find a device by name in the configuration."""
        return self.devices.get(name)

    def list_devices(self):
        """List all configured device names."""
        return list(self.devices.keys())

    def find_command_alias(self, name):
        """Find a command alias by name in the configuration."""
        return self.command_aliases.get(name)

    def list_command_aliases(self):
        """List all configured command alias names."""
        return list(self.command_aliases.keys())

    def find_command_in_search_paths(self, command_name):
        """
        Search for a command in the configured search paths.
        
        Returns:
            Path: Path to the command directory if found, None otherwise
        """
        # Search in configured search paths first
        for search_path in self.search_paths:
            command_path = Path(search_path) / command_name
            if command_path.exists() and command_path.is_dir():
                code_file = command_path / 'code.py'
                if code_file.exists():
                    self.debug(f"Found command '{command_name}' in search path: {search_path}")
                    return command_path
        
        # Search in ~/.circremote/commands
        user_commands_dir = Path.home() / '.circremote' / 'commands'
        if user_commands_dir.exists():
            command_path = user_commands_dir / command_name
            if command_path.exists() and command_path.is_dir():
                code_file = command_path / 'code.py'
                if code_file.exists():
                    self.debug(f"Found command '{command_name}' in user commands: {user_commands_dir}")
                    return command_path
        
        # Not found in search paths
        return None

    def debug(self, message):
        """Print debug message if verbose mode is enabled."""
        if self.options and hasattr(self.options, 'verbose') and self.options.verbose:
            print(message)

    def load_config(self):
        """Load device configuration from JSON file."""
        self.debug(f"Looking for config file at: {self.config_path}")
        
        if not self.config_path.exists():
            self.debug("Config file does not exist")
            return
            
        self.debug("Config file exists")

        # Check file permissions - complain if world accessible
        self.check_file_permissions()

        try:
            with open(self.config_path, 'r') as f:
                config_content = f.read()
                self.debug(f"Read config file, content length: {len(config_content)}")
                config_data = json.loads(config_content)
                self.debug("Parsed JSON successfully")
                
                # Load devices
                if 'devices' in config_data and isinstance(config_data['devices'], list):
                    self.debug(f"Found {len(config_data['devices'])} devices in config")
                    for device in config_data['devices']:
                        self.validate_device_config(device)
                        self.devices[device['name']] = device
                        self.debug(f"Added device: {device['name']} -> {device['device']}")
                else:
                    self.debug("No 'devices' array found in config")
                
                # Load command aliases
                if 'command_aliases' in config_data and isinstance(config_data['command_aliases'], list):
                    self.debug(f"Found {len(config_data['command_aliases'])} command aliases in config")
                    for alias in config_data['command_aliases']:
                        self.validate_command_alias_config(alias)
                        self.command_aliases[alias['name']] = alias['command']
                        self.debug(f"Added command alias: {alias['name']} -> {alias['command']}")
                else:
                    self.debug("No 'command_aliases' array found in config")
                
                # Load search paths
                if 'search_paths' in config_data and isinstance(config_data['search_paths'], list):
                    self.debug(f"Found {len(config_data['search_paths'])} search paths in config")
                    for search_path in config_data['search_paths']:
                        self.validate_search_path_config(search_path)
                        path = Path(search_path).expanduser().resolve()
                        if path.exists() and path.is_dir():
                            self.search_paths.append(str(path))
                            self.debug(f"Added search path: {path}")
                        else:
                            print(f"Warning: Search path '{search_path}' does not exist or is not accessible")
                else:
                    self.debug("No 'search_paths' array found in config")
                
                # Load circup path
                if 'circup' in config_data and isinstance(config_data['circup'], str):
                    self.circup_path = config_data['circup']
                    self.debug(f"Found circup path in config: {self.circup_path}")
                else:
                    self.debug("No 'circup' path found in config")
                    
        except json.JSONDecodeError as e:
            print(f"❌ Error: Config file {self.config_path} contains invalid JSON: {e}")
            import sys
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error: Could not read config file {self.config_path}: {e}")
            import sys
            sys.exit(1)

    def check_file_permissions(self):
        """Check if config file has appropriate permissions."""
        try:
            stat_info = self.config_path.stat()
            current_user = getpass.getuser()
            
            # Get file owner (Unix-like systems)
            try:
                import pwd
                file_owner = pwd.getpwuid(stat_info.st_uid).pw_name
            except (ImportError, KeyError):
                file_owner = "unknown"

            # Check if file is world readable or writable
            if stat_info.st_mode & stat.S_IROTH or stat_info.st_mode & stat.S_IWOTH:
                print(f"Warning: Config file {self.config_path} has world access permissions")
                print(f"  Owner: {file_owner}")
                print(f"  Current user: {current_user}")
                print(f"  Permissions: {oct(stat_info.st_mode)}")
                print(f"  This is a security risk. Consider running: chmod 600 {self.config_path}")
                print()
        except Exception as e:
            print(f"Warning: Could not check file permissions: {e}")

    def validate_device_config(self, device):
        """Validate device configuration structure."""
        if not isinstance(device, dict):
            raise ValueError("Device configuration must be a dictionary")

        if 'name' not in device or not isinstance(device['name'], str):
            raise ValueError("Device configuration must have a 'name' string field")

        if 'device' not in device or not isinstance(device['device'], str):
            raise ValueError("Device configuration must have a 'device' string field")

        # Optional fields
        if 'friendly_name' in device and not isinstance(device['friendly_name'], str):
            raise ValueError("Device 'friendly_name' must be a string")

        if 'password' in device and not isinstance(device['password'], str):
            raise ValueError("Device 'password' must be a string")

    def validate_command_alias_config(self, alias):
        """Validate command alias configuration structure."""
        if not isinstance(alias, dict):
            raise ValueError("Command alias configuration must be a dictionary")

        if 'name' not in alias or not isinstance(alias['name'], str):
            raise ValueError("Command alias configuration must have a 'name' string field")

        if 'command' not in alias or not isinstance(alias['command'], str):
            raise ValueError("Command alias configuration must have a 'command' string field")

    def validate_search_path_config(self, search_path):
        """Validate search path configuration."""
        if not isinstance(search_path, str):
            raise ValueError("Search path must be a string")
        
        if not search_path.strip():
            raise ValueError("Search path cannot be empty")

    def get_circup_path(self):
        """
        Get the circup executable path with precedence:
        1. Command line option (-u)
        2. Config file setting
        3. System PATH resolution (default)
        
        Returns:
            str: Path to circup executable
        """
        # Command line option takes precedence
        if self.options and hasattr(self.options, 'circup') and self.options.circup:
            return self.options.circup
        
        # Config file setting
        if self.circup_path:
            return self.circup_path
        
        # Try to find circup in system PATH
        import shutil
        import os
        
        # In Docker containers, circup is installed at /usr/local/bin/circup
        if os.path.exists('/usr/local/bin/circup'):
            return '/usr/local/bin/circup'
        
        # Try to find circup in PATH
        circup_path = shutil.which('circup')
        if circup_path:
            return circup_path
        
        # Fallback to just 'circup' (will be resolved by subprocess)
        return 'circup' 