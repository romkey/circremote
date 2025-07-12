# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: MIT

import sys
import os
import json
import time
import re
import subprocess
import signal
from pathlib import Path
from argparse import ArgumentParser, Namespace
from typing import Dict, Any, Optional

from .config import Config
from .connection import CircuitPythonConnection


def main():
    """Main entry point for the cpctrl command."""
    cli = CLI()
    cli.run(sys.argv[1:])


class CLI:
    def __init__(self):
        self.config = Config()

    def run(self, args):
        """Run the CLI with the given arguments."""
        options, remaining = self.parse_options(args)
        
        if len(remaining) < 2:
            print("Usage: cpctrl [options] <device_name_or_path> <command_name> [variable=value ...]")
            print("Example: cpctrl /dev/ttyUSB0 BME280")
            print("Example: cpctrl sign-1 BME280 sda=board.IO1 scl=board.IO2")
            print("Example: cpctrl 10.0.1.230:8080 BME280")
            print("Use -h for more options")
            sys.exit(1)

        device_spec = remaining[0]
        command_name = remaining[1]
        
        # Resolve device
        device_info = self.resolve_device(device_spec, options)
        
        serial_port = device_info['device']
        password = device_info.get('password') or options.password
        
        # Parse variable assignments from remaining arguments
        variables = self.parse_command_line_variables(remaining[2:])

        # Check if command directory exists and contains code.py
        commands_dir = Path(__file__).parent.parent / 'commands'
        command_dir = commands_dir / command_name
        code_file = command_dir / 'code.py'

        self.debug(f"Checking if command directory '{command_dir}' exists", options)
        if not command_dir.exists():
            print(f"Error: Command '{command_name}' not found")
            print("Available commands:")
            for cmd in sorted([d.name for d in commands_dir.iterdir() if d.is_dir() and d.name not in ['.', '..']]):
                print(f"  {cmd}")
            sys.exit(1)

        self.debug(f"Command directory '{command_dir}' exists", options)

        self.debug("Checking if code.py exists in command directory", options)
        if not code_file.exists():
            print(f"Error: code.py not found in command directory '{command_dir}'")
            sys.exit(1)
        self.debug("code.py exists in command directory", options)

        # Check for requirements.txt and install dependencies with circup
        requirements_file = command_dir / 'requirements.txt'
        self.debug("Checking for requirements.txt in command directory", options)
        
        if requirements_file.exists() and not options.skip_circup:
            self.debug("requirements.txt found, checking content", options)
            with open(requirements_file, 'r') as f:
                requirements_content = f.read()
            
            # Filter out comments and blank lines to check for actual requirements
            actual_requirements = [
                line.strip() for line in requirements_content.split('\n')
                if line.strip() and not line.strip().startswith('#')
            ]
            
            self.debug(f"Requirements content: {repr(requirements_content)}", options)
            self.debug(f"Actual requirements after filtering: {actual_requirements}", options)
            self.debug(f"Number of actual requirements: {len(actual_requirements)}", options)
            
            if actual_requirements:
                self.debug("requirements.txt has actual content (after filtering comments/blanks), checking for circup", options)
                self.handle_circup_installation(requirements_file, serial_port, password, options)
            else:
                self.debug("requirements.txt has no actual content (only comments/blanks), skipping circup", options)

        # Read and parse info.json file
        info_file = command_dir / 'info.json'
        info_data = None
        self.debug("Reading info.json from command directory", options)
        
        if info_file.exists():
            try:
                with open(info_file, 'r') as f:
                    info_content = f.read()
                    info_data = json.loads(info_content)
                    self.debug("Successfully parsed info.json", options)
                    
                    # Check for warn_offline flag
                    if info_data.get('warn_offline'):
                        self.show_offline_warning(options)
                    
                    # Check for tested flag
                    if info_data.get('tested') is False:
                        self.show_tested_warning(options)
                    
                    # Display module description if available
                    if info_data.get('description'):
                        print(f"Module: {command_name}")
                        print(f"Description: {info_data['description']}")
                        print()
                        
            except json.JSONDecodeError as e:
                print(f"Warning: Could not parse info.json: {e}")
                print("Proceeding without module information...")
            except Exception as e:
                print(f"Warning: Error reading info.json: {e}")
                print("Proceeding without module information...")
        else:
            print(f"Warning: info.json not found in command directory '{command_dir}'")
            print("Proceeding without module information...")

        # Add defaults from info.json for any missing variables
        variables = self.add_defaults_from_info(variables, info_data, command_name)
        
        if variables:
            self.debug(f"Final variables (including defaults): {variables}", options)
            print(f"Variables: {', '.join([f'{k}={v}' for k, v in variables.items()])}")
            print()
            
            # Validate variables against info.json
            self.validate_variables(variables, info_data, command_name)

        # Read the file content
        try:
            self.debug("Reading code.py from command directory", options)
            with open(code_file, 'r') as f:
                file_content = f.read()
            
            self.debug(f"File content length: {len(file_content)} characters", options)
            self.debug(f"File content bytes: {len(file_content.encode('utf-8'))} bytes", options)
            print(f"Read {len(file_content.encode('utf-8'))} bytes from '{command_name}/code.py'")
            
            if options.verbose:
                self.debug("File content preview (first 200 chars):", options)
                preview = file_content[:200]
                preview_lines = preview.split('\n')
                for i, line in enumerate(preview_lines):
                    self.debug(f"  Line {i+1}: {line}", options)
                if len(file_content) > 200:
                    self.debug("  ... (truncated)", options)
                    
        except Exception as e:
            print(f"Error reading code.py: {e}")
            sys.exit(1)

        # Check for template variables and interpolate if needed
        template_vars = re.findall(r'\{\{\s*(\w+)\s*\}\}', file_content)
        if template_vars:
            template_vars = list(set(template_vars))  # Remove duplicates
            self.debug(f"Found template variables in code: {template_vars}", options)
            
            if variables:
                self.debug("Interpolating variables into code content", options)
                file_content = self.interpolate_variables(file_content, variables, info_data, command_name)
                self.debug(f"Code content after interpolation length: {len(file_content)} characters", options)
                self.debug(f"Code content after interpolation bytes: {len(file_content.encode('utf-8'))} bytes", options)
            else:
                print(f"❌ Error: Template variables found in code.py but no variables available (including defaults) for module '{command_name}':")
                for var in template_vars:
                    print(f"   - '{{{{ {var} }}}}' requires a value (e.g., {var}=value)")
                print()
                print("Please provide values for all template variables on the command line.")
                print(f"Example: cpctrl /dev/ttyUSB0 {command_name} {template_vars[0]}=value")
                sys.exit(1)
        else:
            self.debug("No template variables found in code", options)

        # Establish connection using CircuitPythonConnection class
        try:
            self.debug("Establishing CircuitPython connection", options)
            connection = CircuitPythonConnection(
                serial_port, 
                password=password, 
                debug_options=options.__dict__
            )
            connection_type = connection.connection_type
        except Exception as e:
            print(f"Error establishing connection: {e}")
            self.debug(f"Connection error details: {type(e).__name__}: {e}", options)
            sys.exit(1)

        # CircuitPython REPL protocol
        try:
            self.debug("Starting CircuitPython REPL protocol", options)
            
            print("Interrupting CircuitPython (Ctrl+C x3)...")
            self.debug("Sending 3 Ctrl+C characters (\\x03)", options)
            connection.write("\x03\x03\x03")  # Send Ctrl+C three times
            self.debug("Waiting 0.5 seconds after Ctrl+C", options)
            time.sleep(0.5)
            
            print("Entering raw REPL mode (Ctrl+A)...")
            self.debug("Sending Ctrl+A character (\\x01)", options)
            connection.write("\x01")  # Send Ctrl+A
            self.debug("Waiting 0.5 seconds after Ctrl+A", options)
            time.sleep(0.5)
            
            print("Sending start marker...")
            self.debug("Sending: print('***START***')", options)
            start_marker = "print('***START***')\r\n"
            connection.write(start_marker)
            connection.flush()
            self.debug("Start marker sent and flushed", options)
            
            file_content = file_content.replace('\n', '\r\n')

            print("Transmitting Python code...")
            self.debug(f"Transmitting {len(file_content.encode('utf-8'))} bytes of Python code", options)
            if options.verbose:
                self.debug("Code transmission details:", options)
                self.debug(f"  - Characters: {len(file_content)}", options)
                self.debug(f"  - Lines: {len(file_content.split(chr(10)))}", options)
                self.debug(f"  - Bytes: {len(file_content.encode('utf-8'))}", options)
            connection.write(file_content)
            connection.flush()
            self.debug("Python code transmission complete and flushed", options)
            print("Code transmission complete")
            
            print("Sending end marker...")
            self.debug("Sending: print('***END***')", options)
            end_marker = "print('***END***')\r\n"
            connection.write(end_marker)
            connection.flush()
            self.debug("End marker sent and flushed", options)
            
            print("Exiting raw REPL mode (Ctrl+D, Ctrl+B)...")
            self.debug("Sending Ctrl+D character (\\x04)", options)
            connection.write("\x04")  # Send Ctrl+D
            self.debug("Waiting 0.1 seconds after Ctrl+D", options)
            time.sleep(0.1)
            self.debug("Sending Ctrl+B character (\\x02)", options)
            connection.write("\x02")  # Send Ctrl+B
            
            connection.flush()
            self.debug("REPL exit sequence complete and flushed", options)
            print("REPL mode exit complete")
        except Exception as e:
            print(f"Error during CircuitPython communication: {e}")
            self.debug(f"CircuitPython communication error details: {type(e).__name__}: {e}", options)
            if options.verbose:
                import traceback
                self.debug(f"Error backtrace: {traceback.format_exc()}", options)
            connection.close()
            sys.exit(1)

        # Display output from connection for 10 seconds
        print("Listening for output (10 seconds)...")
        print("-" * 50)

        try:
            self.debug("Starting output monitoring with 10-second timeout", options)
            self.monitor_output(connection, options)
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        except Exception as e:
            print(f"\nError reading from connection: {e}")
            self.debug(f"Output reading error details: {type(e).__name__}: {e}", options)
            if options.verbose:
                import traceback
                self.debug(f"Error backtrace: {traceback.format_exc()}", options)
        finally:
            # Handle double exit option after output monitoring
            if options.double_exit:
                self.debug("Double exit mode: waiting 10 seconds before sending additional Ctrl+D", options)
                time.sleep(10)
                self.debug("Sending additional Ctrl+D character (\\x04)", options)
                connection.write("\x04")  # Send additional Ctrl+D
                connection.flush()
                self.debug("Double exit sequence complete", options)
            
            self.debug("Closing connection", options)
            connection.close()
            if connection.connection_type == 'serial':
                print("Serial port closed")
            else:
                print("WebSocket connection closed")

    def parse_options(self, args):
        """Parse command line options."""
        parser = ArgumentParser(
            description="Upload and run Python code on CircuitPython devices",
            add_help=False  # We'll handle help manually
        )
        
        parser.add_argument('-v', '--verbose', action='store_true',
                          help='Enable verbose debug output')
        parser.add_argument('-p', '--password', type=str,
                          help='HTTP basic auth password for WebSocket connections')
        parser.add_argument('-d', '--double-exit', action='store_true',
                          help='Send additional Ctrl+D after Ctrl+B to exit raw REPL')
        parser.add_argument('-C', '--skip-circup', action='store_true',
                          help='Skip circup dependency installation')
        parser.add_argument('-y', '--yes', action='store_true',
                          help='Skip confirmation prompts (run untested commands without asking)')
        parser.add_argument('-h', '--help', action='store_true',
                          help='Show this help message')
        
        try:
            options, remaining = parser.parse_known_args(args)
        except Exception as e:
            print(f"❌ Error parsing options: {e}")
            sys.exit(1)
        
        # Handle help manually
        if options.help:
            self.show_help(parser)
            sys.exit(0)
        
        return options, remaining

    def show_help(self, parser):
        """Show help message with examples."""
        print("Usage: cpctrl [options] <serial_port_or_ip> <command_name> [variable=value ...]")
        print()
        print("Options:")
        print("  -v, --verbose                    Enable verbose debug output")
        print("  -p, --password PASSWORD          HTTP basic auth password for WebSocket connections")
        print("  -d, --double-exit                Send additional Ctrl+D after Ctrl+B to exit raw REPL")
        print("  -C, --skip-circup                Skip circup dependency installation")
        print("  -y, --yes                        Skip confirmation prompts (run untested commands without asking)")
        print("  -h, --help                       Show this help message")
        print()
        print("Examples:")
        print("  cpctrl /dev/ttyUSB0 BME280")
        print("  cpctrl sign-1 BME280                    # Using config device name")
        print("  cpctrl -v /dev/ttyACM0 VL53L1X")
        print("  cpctrl 192.168.1.100 SHT30")
        print("  cpctrl -p mypassword 192.168.1.100:8080 show-settings")
        print("  cpctrl -d /dev/ttyUSB0 system-info")
        print("  cpctrl -v -d -p mypassword 192.168.1.100 scan-i2c")
        print("  cpctrl /dev/ttyUSB0 BME280 sda=board.IO1 scl=board.IO2")
        print("  cpctrl sign-1 BME280 sda=board.IO1 scl=board.IO2  # With variables")
        print("  cpctrl /dev/ttyUSB0 PMS5003 rx=board.TX tx=board.RX")
        print("  cpctrl -C /dev/ttyUSB0 BME280")
        print("  cpctrl -y /dev/ttyUSB0 ADXL345                    # Skip confirmation for untested modules")
        print("\nAvailable commands:")
        
        commands_dir = Path(__file__).parent.parent / 'commands'
        if commands_dir.exists():
            for cmd in sorted([d.name for d in commands_dir.iterdir() if d.is_dir() and d.name not in ['.', '..']]):
                print(f"  {cmd}")

    def parse_command_line_variables(self, args):
        """Parse variable assignments from command line arguments."""
        variables = {}
        
        for arg in args:
            if '=' in arg:
                var_name, value = arg.split('=', 1)
                var_name = var_name.strip()
                value = value.strip()
                
                # Remove quotes if present
                value = value.strip('"\'')
                
                variables[var_name] = value
            else:
                print(f"❌ Error: Invalid variable format '{arg}'")
                print("Variables must be in the format 'variable=value'")
                print("Example: sda=board.IO1 scl=board.IO2")
                sys.exit(1)
        
        return variables

    def debug(self, message, options):
        """Print debug message if verbose mode is enabled."""
        if options and options.verbose:
            print(f"[DEBUG] {message}")

    def validate_variables(self, variables, info_data, command_name):
        """Validate variables against info.json."""
        if not info_data or 'variables' not in info_data:
            return
        
        # Get the list of valid variable names from info.json
        valid_variables = [var['name'] for var in info_data['variables']]
        
        # Check each provided variable against the valid list
        invalid_variables = [var for var in variables.keys() if var not in valid_variables]
        
        if invalid_variables:
            print(f"❌ Error: Invalid variables provided for module '{command_name}':")
            for var in invalid_variables:
                print(f"   - '{var}' is not a valid variable for this module")
            print()
            print("Valid variables for this module:")
            if not valid_variables:
                print("   (none defined)")
            else:
                for var in valid_variables:
                    print(f"   - {var}")
            print()
            print("Please check the module's info.json file for the correct variable names.")
            sys.exit(1)

    def add_defaults_from_info(self, variables, info_data, command_name):
        """Add default values from info.json for missing variables."""
        if not info_data or 'variables' not in info_data:
            return variables
        
        # Create a copy of the variables dict
        result = variables.copy()
        
        # Add defaults for any missing variables
        for var in info_data['variables']:
            var_name = var['name']
            if var_name not in result:  # Skip if already provided
                if 'default' in var:
                    default_value = var['default']
                    if default_value is not None:
                        result[var_name] = str(default_value)
                        self.debug(f"Added default '{default_value}' for variable '{var_name}'", None)
        
        return result

    def interpolate_variables(self, content, variables, info_data, command_name):
        """Interpolate variables into template content."""
        # Get the list of valid variable names from info.json
        valid_variables = []
        if info_data and 'variables' in info_data:
            valid_variables = [var['name'] for var in info_data['variables']]
        
        # Find all template variables in the content
        template_vars = re.findall(r'\{\{\s*(\w+)\s*\}\}', content)
        template_vars = list(set(template_vars))  # Remove duplicates
        
        # Check if any template variables are not in the valid list
        invalid_template_vars = [var for var in template_vars if var not in valid_variables]
        if invalid_template_vars:
            print(f"❌ Error: Template variables found in code.py that are not defined in info.json for module '{command_name}':")
            for var in invalid_template_vars:
                print(f"   - '{{{{ {var} }}}}' is not a valid variable for this module")
            print()
            print("Valid variables for this module:")
            if not valid_variables:
                print("   (none defined)")
            else:
                for var in valid_variables:
                    print(f"   - {var}")
            print()
            print("Please update the module's info.json file to include these variables.")
            sys.exit(1)
        
        # Check if any template variables are not provided in command line
        missing_vars = [var for var in template_vars if var not in variables]
        if missing_vars:
            print(f"❌ Error: Template variables found in code.py but not provided on command line for module '{command_name}':")
            for var in missing_vars:
                print(f"   - '{{{{ {var} }}}}' requires a value (e.g., {var}=value)")
            print()
            print("Please provide values for all template variables on the command line.")
            sys.exit(1)
        
        # Perform the interpolation
        result = content
        for var_name, value in variables.items():
            pattern = r'\{\{\s*' + re.escape(var_name) + r'\s*\}\}'
            result = re.sub(pattern, value, result)
        
        return result

    def resolve_device(self, device_spec, options):
        """Resolve device specification to device info."""
        # First, try to find the device in the config
        device_config = self.config.find_device(device_spec)
        
        if device_config:
            self.debug(f"Found device '{device_spec}' in config: {device_config['device']}", options)
            return device_config
        
        # If not found in config, treat as direct device specification
        self.debug(f"Device '{device_spec}' not found in config, treating as direct specification", options)
        return {
            'name': device_spec,
            'device': device_spec
        }

    def show_offline_warning(self, options):
        """Show warning for modules that may make device unreachable."""
        print("\n" + "="*60)
        print("⚠️  WARNING: This module may make the CircuitPython device")
        print("   unreachable without physical access to it.")
        print("="*60)
        print()
        print("This could happen if the code:")
        print("  • Enters a deep sleep mode")
        print("  • Disables USB communication")
        print("  • Changes boot behavior")
        print("  • Enters a low-power state")
        print("  • Disconnects from the network")
        print()
        
        if not options.yes:
            response = input("Do you want to run this code anyway? (y/N): ").strip().lower()
            if response not in ['y', 'yes']:
                print("Operation cancelled by user.")
                sys.exit(0)
            print("Proceeding with code execution...")
            print()

    def show_tested_warning(self, options):
        """Show warning for untested modules."""
        print("\n" + "="*60)
        print("⚠️  WARNING: This module has not been tested")
        print("="*60)
        print()
        print("This module is marked as untested and may:")
        print("  • Not work as expected")
        print("  • Have incorrect pin assignments")
        print("  • Use wrong I2C addresses")
        print("  • Have missing dependencies")
        print("  • Cause unexpected behavior")
        print()
        
        if options.yes:
            print("Proceeding without confirmation due to -y flag...")
            print()
        else:
            response = input("Do you want to run this untested code anyway? (y/N): ").strip().lower()
            if response not in ['y', 'yes']:
                print("Operation cancelled by user.")
                sys.exit(0)
            print("Proceeding with untested code execution...")
            print()

    def handle_circup_installation(self, requirements_file, serial_port, password, options):
        """Handle circup dependency installation."""
        # Check if circup exists and is executable
        circup_path = None
        for path in ['circup', '/usr/local/bin/circup', '/opt/homebrew/bin/circup']:
            if os.path.exists(path) and os.access(path, os.X_OK):
                circup_path = path
                break
        
        if not circup_path:
            print("⚠️  Warning: requirements.txt found but 'circup' not found or not executable")
            print("   Please install circup to automatically install dependencies:")
            print("   pip install circup")
            print("   Continuing without installing dependencies...")
            print()
            return
        
        self.debug(f"Found circup at: {circup_path}", options)
        
        # Build circup command
        circup_args = []
        # Add WebSocket-specific arguments if using WebSocket
        if re.match(r'^(\d{1,3}\.){3}\d{1,3}(:\d+)?$', serial_port):
            self.debug("Detected WebSocket connection, adding host/port/password args", options)
            if ':' in serial_port:
                host, port = serial_port.split(':', 1)
            else:
                host = serial_port
                port = "80"  # Default port if not specified
            
            circup_args += ["--host", host, "--port", port]
            if password:
                circup_args += ["--password", password]
        
        circup_args += ["install", "-r", str(requirements_file)]
        full_command = [circup_path] + circup_args
        command_string = " ".join(full_command)
        
        print("\n" + "="*60)
        print("📦 DEPENDENCIES FOUND")
        print("="*60)
        print()
        print("This module requires CircuitPython libraries to be installed.")
        print(f"Requirements file: {requirements_file}")
        print()
        print("The following command will be executed:")
        print(f"  {command_string}")
        print()
        print("Options:")
        print("  r - run (install dependencies and continue)")
        print("  s - skip (continue without installing dependencies)")
        print("  x - exit (cancel operation)")
        print()
        
        if options.yes:
            print("Installing dependencies automatically due to -y flag...")
            self.run_circup_command(full_command, options)
        else:
            response = input("What would you like to do? (r/s/x): ").strip().lower()
            
            if response in ['r', 'run']:
                print("Installing dependencies...")
                self.run_circup_command(full_command, options)
            elif response in ['s', 'skip']:
                print("Skipping dependency installation...")
                print()
            elif response in ['x', 'exit']:
                print("Operation cancelled by user.")
                sys.exit(0)
            else:
                print("Invalid option. Cancelling operation.")
                sys.exit(0)

    def run_circup_command(self, full_command, options):
        """Run the circup command."""
        self.debug(f"Executing circup command: {' '.join(full_command)}", options)
        
        try:
            result = subprocess.run(full_command, capture_output=True, text=True)
            
            # Display circup output
            if result.stdout:
                print("Circup output:")
                print("-" * 40)
                print(result.stdout)
                print("-" * 40)
            
            if result.stderr:
                print("Circup error output:")
                print("-" * 40)
                print(result.stderr)
                print("-" * 40)
            
            if result.returncode == 0:
                print("✅ Dependencies installed successfully")
                self.debug("Circup command completed successfully", options)
            else:
                print(f"❌ Failed to install dependencies (exit code: {result.returncode})")
                self.debug(f"Circup command failed with exit code: {result.returncode}", options)
                print("Continuing anyway...")
        except Exception as e:
            print(f"❌ Error running circup: {e}")
            self.debug(f"Circup execution error: {type(e).__name__}: {e}", options)
            print("Continuing anyway...")
        print()

    def monitor_output(self, connection, options):
        """Monitor output from the connection for 10 seconds."""
        import signal
        
        # Set up timeout
        def timeout_handler(signum, frame):
            raise TimeoutError("Timeout reached")
        
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(10)
        
        try:
            if connection.connection_type == 'serial':
                self.monitor_serial_output(connection, options)
            else:
                self.monitor_websocket_output(connection, options)
        finally:
            signal.alarm(0)  # Cancel the alarm

    def monitor_serial_output(self, connection, options):
        """Monitor output from serial connection."""
        buffer = ""
        found_start = False
        found_end = False
        bytes_read = 0
        read_count = 0
        
        self.debug(f"Initial state: buffer='{buffer}', found_start={found_start}, found_end={found_end}", options)
        
        while True:
            try:
                data = connection.read_nonblock(1024)
                if not data:
                    time.sleep(0.1)
                    continue
                    
                bytes_read += len(data.encode('utf-8'))
                read_count += 1
                self.debug(f"Read {len(data.encode('utf-8'))} bytes (total: {bytes_read}, reads: {read_count})", options)
                if options.verbose:
                    self.debug(f"Raw data: {repr(data)}", options)
                
                buffer += data
                self.debug(f"Buffer length: {len(buffer)} characters", options)
                
                # Look for ***START*** marker
                if not found_start and "***START***" in buffer:
                    start_index = buffer.index("***START***")
                    self.debug(f"Found ***START*** marker at index {start_index}", options)
                    
                    # Check if ***END*** is also in this buffer
                    if "***END***" in buffer:
                        end_index = buffer.index("***END***")
                        self.debug(f"Found ***END*** marker at index {end_index} in same buffer", options)
                        
                        # Only display content between ***START*** and ***END***
                        display_start = start_index + len("***START***")
                        display_end = end_index
                        if display_start < display_end:
                            display_content = buffer[display_start:display_end]
                            self.debug(f"Content between markers: {repr(display_content)}", options)
                            if display_content.strip():
                                self.debug("Displaying content between markers", options)
                                print(display_content, end='', flush=True)
                        
                        found_start = True
                        found_end = True
                        self.debug("Set found_start=true, found_end=true, breaking loop", options)
                        break
                    else:
                        # Only ***START*** found, display content after it
                        display_content = buffer[start_index + len("***START***"):]
                        self.debug(f"Content after ***START***: {repr(display_content)}", options)
                        if display_content.strip():
                            self.debug("Displaying content after ***START***", options)
                            print(display_content, end='', flush=True)
                        found_start = True
                        buffer = ""
                        self.debug("Set found_start=true, cleared buffer", options)
                elif found_start and not found_end:
                    # Look for ***END*** marker
                    if "***END***" in buffer:
                        end_index = buffer.index("***END***")
                        self.debug(f"Found ***END*** marker at index {end_index}", options)
                        # Display content up to ***END***
                        display_content = buffer[:end_index]
                        self.debug(f"Content before ***END***: {repr(display_content)}", options)
                        if display_content.strip():
                            self.debug("Displaying content before ***END***", options)
                            print(display_content, end='', flush=True)
                        found_end = True
                        self.debug("Set found_end=true, breaking loop", options)
                        break
                    else:
                        # Display all content since we're between markers
                        self.debug(f"Displaying buffer content (between markers): {repr(buffer)}", options)
                        print(buffer, end='', flush=True)
                        buffer = ""
                        self.debug("Cleared buffer after display", options)
                else:
                    self.debug(f"Skipping data (found_start={found_start}, found_end={found_end})", options)
                    
            except Exception as e:
                if "timeout" in str(e).lower():
                    break
                time.sleep(0.1)
        
        self.debug("Output monitoring complete", options)
        self.debug(f"Final stats: bytes_read={bytes_read}, read_count={read_count}", options)

    def monitor_websocket_output(self, connection, options):
        """Monitor output from WebSocket connection."""
        buffer = ""
        found_start = False
        found_end = False
        bytes_read = 0
        message_count = 0
        
        self.debug(f"Initial WebSocket state: buffer='{buffer}', found_start={found_start}, found_end={found_end}", options)
        
        # Set up message handler for WebSocket
        def message_handler(msg):
            nonlocal buffer, found_start, found_end, bytes_read, message_count
            message_count += 1
            data = msg.data if hasattr(msg, 'data') else str(msg)
            bytes_read += len(data.encode('utf-8'))
            self.debug(f"WebSocket received {len(data.encode('utf-8'))} bytes (total: {bytes_read}, messages: {message_count})", options)
            if options.verbose:
                self.debug(f"Raw WebSocket data: {repr(data)}", options)
            
            buffer += data
            self.debug(f"Buffer length: {len(buffer)} characters", options)
            
            # Look for ***START*** marker
            if not found_start and "***START***" in buffer:
                start_index = buffer.index("***START***")
                self.debug(f"Found ***START*** marker at index {start_index}", options)
                
                # Check if ***END*** is also in this buffer
                if "***END***" in buffer:
                    end_index = buffer.index("***END***")
                    self.debug(f"Found ***END*** marker at index {end_index} in same buffer", options)
                    
                    # Only display content between ***START*** and ***END***
                    display_start = start_index + len("***START***")
                    display_end = end_index
                    if display_start < display_end:
                        display_content = buffer[display_start:display_end]
                        self.debug(f"Content between markers: {repr(display_content)}", options)
                        if display_content.strip():
                            self.debug("Displaying content between markers", options)
                            print(display_content, end='', flush=True)
                    
                    found_start = True
                    found_end = True
                    self.debug("Set found_start=true, found_end=true, WebSocket monitoring complete", options)
                else:
                    # Only ***START*** found, display content after it
                    display_content = buffer[start_index + len("***START***"):]
                    self.debug(f"Content after ***START***: {repr(display_content)}", options)
                    if display_content.strip():
                        self.debug("Displaying content after ***START***", options)
                        print(display_content, end='', flush=True)
                    found_start = True
                    buffer = ""
                    self.debug("Set found_start=true, cleared buffer", options)
            elif found_start and not found_end:
                # Look for ***END*** marker
                if "***END***" in buffer:
                    end_index = buffer.index("***END***")
                    self.debug(f"Found ***END*** marker at index {end_index}", options)
                    # Display content up to ***END***
                    display_content = buffer[:end_index]
                    self.debug(f"Content before ***END***: {repr(display_content)}", options)
                    if display_content.strip():
                        self.debug("Displaying content before ***END***", options)
                        print(display_content, end='', flush=True)
                    found_end = True
                    self.debug("Set found_end=true, WebSocket monitoring complete", options)
                else:
                    # Display all content since we're between markers
                    self.debug(f"Displaying buffer content (between markers): {repr(buffer)}", options)
                    print(buffer, end='', flush=True)
                    buffer = ""
                    self.debug("Cleared buffer after display", options)
            else:
                self.debug(f"Skipping data (found_start={found_start}, found_end={found_end})", options)
        
        connection.on_message(message_handler)
        
        # Wait for output with timeout
        start_time = time.time()
        while time.time() - start_time < 10:
            if found_end:
                break
            time.sleep(0.1)
        
        self.debug("WebSocket output monitoring complete", options)
        self.debug(f"Final WebSocket stats: bytes_read={bytes_read}, message_count={message_count}", options) 