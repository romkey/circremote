# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: MIT

import re
import time
import base64
import serial
import websocket
import threading
from urllib.parse import urlparse


class CircuitPythonConnection:
    def __init__(self, connection_string, password=None, debug_options=None):
        self.connection_string = connection_string
        self.password = password
        self.debug_options = debug_options or {}
        self.connection = None
        self.connection_type = None
        self.ws_messages = []
        self.ws_message_handlers = []
        self.ws_error_handlers = []
        self.ws_close_handlers = []
        
        self.establish_connection()

    def write(self, data):
        """Write data to the connection."""
        self.debug(f"Writing {len(data)} bytes")
        if self.connection_type == 'serial':
            self.connection.write(data.encode('utf-8'))
        else:
            self.connection.send(data)

    def flush(self):
        """Flush the connection buffer."""
        if self.connection_type == 'serial':
            self.connection.flush()
        # WebSocket doesn't need explicit flush

    def close(self):
        """Close the connection."""
        self.debug(f"Closing {self.connection_type} connection")
        if self.connection:
            if self.connection_type == 'serial':
                self.connection.close()
            else:
                self.connection.close()

    def read_nonblock(self, max_bytes=1024):
        """Read data from serial connection (non-blocking)."""
        if self.connection_type == 'serial':
            return self.connection.read(max_bytes).decode('utf-8', errors='ignore')
        else:
            raise RuntimeError("read_nonblock not supported for WebSocket connections")

    def on_message(self, handler):
        """Register a message handler for WebSocket connections."""
        if self.connection_type == 'websocket':
            self.ws_message_handlers.append(handler)
        else:
            raise RuntimeError("on_message only supported for WebSocket connections")

    def on_error(self, handler):
        """Register an error handler for WebSocket connections."""
        if self.connection_type == 'websocket':
            self.ws_error_handlers.append(handler)
        else:
            raise RuntimeError("on_error only supported for WebSocket connections")

    def on_close(self, handler):
        """Register a close handler for WebSocket connections."""
        if self.connection_type == 'websocket':
            self.ws_close_handlers.append(handler)
        else:
            raise RuntimeError("on_close only supported for WebSocket connections")

    def establish_connection(self):
        """Establish the appropriate connection type."""
        if self.is_websocket_connection(self.connection_string):
            self.establish_websocket_connection()
        else:
            self.establish_serial_connection()

    def establish_websocket_connection(self):
        """Establish WebSocket connection."""
        self.debug("Establishing WebSocket connection")
        self.connection_type = 'websocket'
        
        host, port = self.parse_websocket_connection(self.connection_string)
        self.debug(f"Parsed WebSocket connection: host={host}, port={port}")
        
        # Build WebSocket URL
        protocol = 'wss' if port == 443 else 'ws'
        ws_url = f"{protocol}://{host}:{port}/cp/serial/"
        self.debug(f"WebSocket URL: {ws_url}")
        
        # Prepare headers for basic auth if password provided
        headers = {}
        if self.password:
            auth_string = base64.b64encode(f":{self.password}".encode()).decode()
            headers['Authorization'] = f"Basic {auth_string}"
            self.debug("Added basic auth header")
        
        # Track connection status
        connection_error = None
        connection_established = False
        
        def on_error(ws, error):
            nonlocal connection_error
            connection_error = error
            self.debug(f"WebSocket connection error: {error}")
            
            # Check for 401 unauthorized error
            if hasattr(error, 'status_code') and error.status_code == 401:
                connection_error = "Bad password - authentication failed"
            elif hasattr(error, 'args') and len(error.args) > 0:
                error_str = str(error.args[0])
                if '401' in error_str or 'unauthorized' in error_str.lower():
                    connection_error = "Bad password - authentication failed"
            # Check for connection refused error
            elif isinstance(error, ConnectionRefusedError):
                connection_error = "Connection refused"
            elif hasattr(error, 'args') and len(error.args) > 0:
                error_str = str(error.args[0])
                if 'connection refused' in error_str.lower() or 'refused' in error_str.lower():
                    connection_error = "Connection refused"
        
        def on_open(ws):
            nonlocal connection_established
            connection_established = True
            self.debug("WebSocket connection opened successfully")
        
        try:
            self.debug("Attempting to connect to WebSocket")
            
            # Create WebSocket connection
            self.connection = websocket.WebSocketApp(
                ws_url,
                header=headers,
                on_open=on_open,
                on_message=self._on_ws_message,
                on_error=on_error,
                on_close=self._on_ws_close
            )
            
            # Start WebSocket in a separate thread
            ws_thread = threading.Thread(target=self.connection.run_forever)
            ws_thread.daemon = True
            ws_thread.start()
            
            # Wait for connection to establish or fail
            timeout = 5  # 5 second timeout
            start_time = time.time()
            while not connection_established and connection_error is None:
                if time.time() - start_time > timeout:
                    connection_error = "Connection timeout"
                    break
                time.sleep(0.1)
            
            # Check for connection errors
            if connection_error:
                error_str = str(connection_error)
                if "Bad password" in error_str:
                    print(f"❌ {error_str}")
                    print("Please check your password and try again.")
                    print("Use the -p option to specify the correct password:")
                    print(f"  circremote -p <password> {self.connection_string} <command>")
                elif "Connection refused" in error_str:
                    print(f"❌ {error_str}")
                    print("The connection was refused. This could be due to:")
                    print("  • Incorrect IP address or hostname")
                    print("  • Wrong port number")
                    print("  • Device not running CircuitPython Web Workflow")
                    print("  • Firewall blocking the connection")
                    print()
                    print("To enable Web Workflow on your CircuitPython device:")
                    print("  • Visit: https://docs.circuitpython.org/en/latest/docs/workflow.html")
                    print("  • Add 'CIRCUITPY_WEB_API_PASSWORD = \"your_password\"' to boot.py")
                    print("  • Restart the device")
                    print()
                    print("Check your connection string and try again:")
                    print(f"  circremote {self.connection_string} <command>")
                else:
                    print(f"Error connecting to WebSocket: {error_str}")
                self.debug(f"WebSocket connection failed: {error_str}")
                raise RuntimeError(error_str)
            
            if connection_established:
                self.debug("WebSocket connection established")
                if self.debug_options and self.debug_options.get('verbose'):
                    print(f"Connected to CircuitPython Web Workflow at {host}:{port}")
            else:
                raise RuntimeError("WebSocket connection failed to establish")
                
        except Exception as e:
            error_str = str(e)
            if "Bad password" in error_str:
                # Already handled above, don't show duplicate message
                pass
            elif isinstance(e, ConnectionRefusedError) or "ConnectionRefusedError" in error_str:
                print("❌ Connection refused")
                print("The connection was refused. This could be due to:")
                print("  • Incorrect IP address or hostname")
                print("  • Wrong port number")
                print("  • Device not running CircuitPython Web Workflow")
                print("  • Firewall blocking the connection")
                print()
                print("To enable Web Workflow on your CircuitPython device:")
                print("  • Visit: https://docs.circuitpython.org/en/latest/docs/workflow.html")
                print("  • Add 'CIRCUITPY_WEB_API_PASSWORD = \"your_password\"' to boot.py")
                print("  • Restart the device")
                print()
                print("Check your connection string and try again:")
                print(f"  circremote {self.connection_string} <command>")
            else:
                print(f"Error connecting to WebSocket: {e}")
                self.debug(f"WebSocket error details: {type(e).__name__}: {e}")
            raise

    def establish_serial_connection(self):
        """Establish serial connection."""
        self.debug("Establishing serial connection")
        self.connection_type = 'serial'
        
        try:
            self.debug(f"Attempting to open serial port '{self.connection_string}'")
            self.debug("Serial port settings: 115200 bps, 8 data bits, 1 stop bit, no parity")
            
            self.connection = serial.Serial(
                port=self.connection_string,
                baudrate=115200,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1
            )
            
            self.debug("Serial port opened successfully")
            if self.debug_options and self.debug_options.get('verbose'):
                print(f"Opened serial port {self.connection_string} at 115200 bps")
            
        except Exception as e:
            print(f"Error opening serial port: {e}")
            self.debug(f"Serial port error details: {type(e).__name__}: {e}")
            raise

    def is_websocket_connection(self, connection_string):
        """Check if connection string looks like an IP address."""
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}(:\d+)?$'
        return bool(re.match(ip_pattern, connection_string))

    def parse_websocket_connection(self, connection_string):
        """Parse WebSocket connection string into host and port."""
        if ':' in connection_string:
            host, port = connection_string.split(':', 1)
            port = int(port)
        else:
            host = connection_string
            port = 80  # Default HTTP port
        
        return host, port

    def _on_ws_message(self, ws, message):
        """Handle WebSocket message events."""
        self.debug(f"WebSocket message received: {message}")
        for handler in self.ws_message_handlers:
            try:
                handler(message)
            except Exception as e:
                self.debug(f"Error in WebSocket message handler: {e}")

    def _on_ws_error(self, ws, error):
        """Handle WebSocket error events."""
        if self.debug_options.get('verbose'):
            print(f"WebSocket error: {error}")
        for handler in self.ws_error_handlers:
            try:
                handler(error)
            except Exception as e:
                self.debug(f"Error in WebSocket error handler: {e}")

    def _on_ws_close(self, ws, close_status_code, close_msg):
        """Handle WebSocket close events."""
        if self.debug_options.get('verbose'):
            print(f"WebSocket closed: {close_status_code} - {close_msg}")
        for handler in self.ws_close_handlers:
            try:
                handler(close_status_code, close_msg)
            except Exception as e:
                self.debug(f"Error in WebSocket close handler: {e}")

    def debug(self, message):
        """Print debug message if verbose mode is enabled."""
        if self.debug_options.get('verbose'):
            print(message) 