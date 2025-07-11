# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: MIT

import json
import os
import stat
import getpass
from pathlib import Path


class Config:
    def __init__(self):
        self.config_path = Path.home() / '.cpctrl' / 'config.json'
        self.devices = {}
        self.load_config()

    def find_device(self, name):
        """Find a device by name in the configuration."""
        return self.devices.get(name)

    def list_devices(self):
        """List all configured device names."""
        return list(self.devices.keys())

    def load_config(self):
        """Load device configuration from JSON file."""
        print(f"[DEBUG] Looking for config file at: {self.config_path}")
        
        if not self.config_path.exists():
            print("[DEBUG] Config file does not exist")
            return
            
        print("[DEBUG] Config file exists")

        # Check file permissions - complain if world accessible
        self.check_file_permissions()

        try:
            with open(self.config_path, 'r') as f:
                config_content = f.read()
                print(f"[DEBUG] Read config file, content length: {len(config_content)}")
                config_data = json.loads(config_content)
                print("[DEBUG] Parsed JSON successfully")
                
                if 'devices' in config_data and isinstance(config_data['devices'], list):
                    print(f"[DEBUG] Found {len(config_data['devices'])} devices in config")
                    for device in config_data['devices']:
                        self.validate_device_config(device)
                        self.devices[device['name']] = device
                        print(f"[DEBUG] Added device: {device['name']} -> {device['device']}")
                else:
                    print("[DEBUG] No 'devices' array found in config")
                    
        except json.JSONDecodeError as e:
            print(f"Warning: Could not parse config file {self.config_path}: {e}")
        except Exception as e:
            print(f"Warning: Error reading config file {self.config_path}: {e}")

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