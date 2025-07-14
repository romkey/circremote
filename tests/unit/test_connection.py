"""
Unit tests for the CircuitPythonConnection class.
"""

import pytest
import serial
import websocket
from unittest.mock import Mock, patch, MagicMock
from argparse import Namespace

from cpctrl.connection import CircuitPythonConnection


class TestCircuitPythonConnection:
    """Test the CircuitPythonConnection class."""

    def test_init_serial_connection(self):
        """Test initialization of serial connection."""
        with patch('serial.Serial') as mock_serial:
            mock_serial.return_value = Mock()
            
            connection = CircuitPythonConnection('/dev/ttyUSB0')
            
            assert connection.connection_type == 'serial'
            mock_serial.assert_called_once_with(
                port='/dev/ttyUSB0',
                baudrate=115200,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1
            )

    def test_init_websocket_connection(self):
        """Test initialization of WebSocket connection."""
        with patch('websocket.WebSocketApp') as mock_ws_app, \
             patch('threading.Thread') as mock_thread:
            mock_ws_app.return_value = Mock()
            mock_thread.return_value = Mock()
            
            connection = CircuitPythonConnection('192.168.1.100:8080')
            
            assert connection.connection_type == 'websocket'
            mock_ws_app.assert_called_once()

    def test_init_websocket_connection_with_password(self):
        """Test initialization of WebSocket connection with password."""
        with patch('websocket.WebSocketApp') as mock_ws_app, \
             patch('threading.Thread') as mock_thread:
            mock_ws_app.return_value = Mock()
            mock_thread.return_value = Mock()
            
            connection = CircuitPythonConnection('192.168.1.100:8080', password='testpass')
            
            assert connection.connection_type == 'websocket'
            # Check that headers were set for basic auth
            mock_ws_app.assert_called_once()
            call_kwargs = mock_ws_app.call_args[1]
            assert 'header' in call_kwargs
            headers = call_kwargs['header']
            assert any('Authorization' in header for header in headers)

    def test_write_serial(self):
        """Test writing to serial connection."""
        with patch('serial.Serial') as mock_serial:
            mock_serial_instance = Mock()
            mock_serial.return_value = mock_serial_instance
            
            connection = CircuitPythonConnection('/dev/ttyUSB0')
            connection.write('test data')
            
            mock_serial_instance.write.assert_called_once_with(b'test data')

    def test_write_websocket(self):
        """Test writing to WebSocket connection."""
        with patch('websocket.WebSocketApp') as mock_ws_app, \
             patch('threading.Thread') as mock_thread:
            mock_ws_app_instance = Mock()
            mock_ws_app.return_value = mock_ws_app_instance
            mock_thread.return_value = Mock()
            
            connection = CircuitPythonConnection('192.168.1.100:8080')
            connection.write('test data')
            
            mock_ws_app_instance.send.assert_called_once_with('test data')

    def test_read_nonblock_serial(self):
        """Test reading from serial connection."""
        with patch('serial.Serial') as mock_serial:
            mock_serial_instance = Mock()
            mock_serial_instance.read.return_value = b'test data'
            mock_serial.return_value = mock_serial_instance
            
            connection = CircuitPythonConnection('/dev/ttyUSB0')
            result = connection.read_nonblock(1024)
            
            assert result == 'test data'
            mock_serial_instance.read.assert_called_once_with(1024)

    def test_read_nonblock_serial_no_data(self):
        """Test reading from serial when no data is available."""
        with patch('serial.Serial') as mock_serial:
            mock_serial_instance = Mock()
            mock_serial_instance.read.return_value = b''
            mock_serial.return_value = mock_serial_instance
            
            connection = CircuitPythonConnection('/dev/ttyUSB0')
            result = connection.read_nonblock(1024)
            
            assert result == ''
            mock_serial_instance.read.assert_called_once_with(1024)

    def test_read_nonblock_websocket_raises_error(self):
        """Test that read_nonblock raises error for WebSocket connections."""
        with patch('websocket.WebSocketApp') as mock_ws_app, \
             patch('threading.Thread') as mock_thread:
            mock_ws_app.return_value = Mock()
            mock_thread.return_value = Mock()
            
            connection = CircuitPythonConnection('192.168.1.100:8080')
            
            with pytest.raises(RuntimeError, match="read_nonblock not supported for WebSocket connections"):
                connection.read_nonblock(1024)

    def test_flush_serial(self):
        """Test flushing serial connection."""
        with patch('serial.Serial') as mock_serial:
            mock_serial_instance = Mock()
            mock_serial.return_value = mock_serial_instance
            
            connection = CircuitPythonConnection('/dev/ttyUSB0')
            connection.flush()
            
            mock_serial_instance.flush.assert_called_once()

    def test_flush_websocket(self):
        """Test flushing WebSocket connection (should do nothing)."""
        with patch('websocket.WebSocketApp') as mock_ws_app, \
             patch('threading.Thread') as mock_thread:
            mock_ws_app.return_value = Mock()
            mock_thread.return_value = Mock()
            
            connection = CircuitPythonConnection('192.168.1.100:8080')
            # Should not raise an exception
            connection.flush()

    def test_close_serial(self):
        """Test closing serial connection."""
        with patch('serial.Serial') as mock_serial:
            mock_serial_instance = Mock()
            mock_serial.return_value = mock_serial_instance
            
            connection = CircuitPythonConnection('/dev/ttyUSB0')
            connection.close()
            
            mock_serial_instance.close.assert_called_once()

    def test_close_websocket(self):
        """Test closing WebSocket connection."""
        with patch('websocket.WebSocketApp') as mock_ws_app, \
             patch('threading.Thread') as mock_thread:
            mock_ws_app_instance = Mock()
            mock_ws_app.return_value = mock_ws_app_instance
            mock_thread.return_value = Mock()
            
            connection = CircuitPythonConnection('192.168.1.100:8080')
            connection.close()
            
            mock_ws_app_instance.close.assert_called_once()

    def test_on_message_websocket(self):
        """Test setting message handler for WebSocket."""
        with patch('websocket.WebSocketApp') as mock_ws_app, \
             patch('threading.Thread') as mock_thread:
            mock_ws_app.return_value = Mock()
            mock_thread.return_value = Mock()
            
            connection = CircuitPythonConnection('192.168.1.100:8080')
            
            def message_handler(msg):
                pass
            
            connection.on_message(message_handler)
            
            # Should add handler to the list
            assert len(connection.ws_message_handlers) == 1
            assert connection.ws_message_handlers[0] == message_handler

    def test_on_message_serial_raises_error(self):
        """Test that on_message raises error for serial connections."""
        with patch('serial.Serial') as mock_serial:
            mock_serial.return_value = Mock()
            
            connection = CircuitPythonConnection('/dev/ttyUSB0')
            
            def message_handler(msg):
                pass
            
            with pytest.raises(RuntimeError, match="on_message only supported for WebSocket connections"):
                connection.on_message(message_handler)

    def test_connection_error_serial(self):
        """Test handling of serial connection errors."""
        with patch('serial.Serial') as mock_serial:
            mock_serial.side_effect = serial.SerialException("Port not found")
            
            with pytest.raises(serial.SerialException):
                CircuitPythonConnection('/dev/ttyUSB0')

    def test_connection_error_websocket(self):
        """Test handling of WebSocket connection errors."""
        with patch('websocket.WebSocketApp') as mock_ws_app:
            mock_ws_app.side_effect = Exception("Connection failed")
            
            with pytest.raises(Exception):
                CircuitPythonConnection('192.168.1.100:8080')

    def test_debug_options_serial(self):
        """Test that debug options are handled for serial connections."""
        debug_options = {'verbose': True, 'password': None}
        
        with patch('serial.Serial') as mock_serial:
            mock_serial.return_value = Mock()
            
            connection = CircuitPythonConnection('/dev/ttyUSB0', debug_options=debug_options)
            
            assert connection.debug_options == debug_options

    def test_debug_options_websocket(self):
        """Test that debug options are handled for WebSocket connections."""
        debug_options = {'verbose': True, 'password': 'testpass'}
        
        with patch('websocket.WebSocketApp') as mock_ws_app, \
             patch('threading.Thread') as mock_thread:
            mock_ws_app.return_value = Mock()
            mock_thread.return_value = Mock()
            
            connection = CircuitPythonConnection('192.168.1.100:8080', debug_options=debug_options)
            
            assert connection.debug_options == debug_options

    def test_websocket_url_parsing(self):
        """Test WebSocket URL parsing."""
        test_cases = [
            ('192.168.1.100', 'ws://192.168.1.100:80/cp/serial/'),
            ('192.168.1.100:8080', 'ws://192.168.1.100:8080/cp/serial/'),
        ]
        
        for input_url, expected_url in test_cases:
            with patch('websocket.WebSocketApp') as mock_ws_app, \
                 patch('threading.Thread') as mock_thread:
                mock_ws_app.return_value = Mock()
                mock_thread.return_value = Mock()
                
                connection = CircuitPythonConnection(input_url)
                
                # Verify the WebSocket URL was constructed correctly
                mock_ws_app.assert_called_once()
                call_args = mock_ws_app.call_args[0]
                assert call_args[0] == expected_url

    def test_websocket_headers_with_password(self):
        """Test WebSocket headers when password is provided."""
        with patch('websocket.WebSocketApp') as mock_ws_app, \
             patch('threading.Thread') as mock_thread:
            mock_ws_app.return_value = Mock()
            mock_thread.return_value = Mock()
            
            connection = CircuitPythonConnection('192.168.1.100:8080', password='testpass')
            
            # Verify headers were set for basic auth
            mock_ws_app.assert_called_once()
            call_kwargs = mock_ws_app.call_args[1]
            assert 'header' in call_kwargs
            headers = call_kwargs['header']
            assert any('Authorization' in header for header in headers)

    def test_is_websocket_connection(self):
        """Test IP address detection for WebSocket connections."""
        with patch('serial.Serial') as mock_serial:
            mock_serial.return_value = Mock()
            connection = CircuitPythonConnection('/dev/ttyUSB0')  # Any connection will do
            
            # Test IP addresses
            assert connection.is_websocket_connection('192.168.1.100')
            assert connection.is_websocket_connection('10.0.0.1')
            assert connection.is_websocket_connection('172.16.0.1:8080')
            assert connection.is_websocket_connection('192.168.1.100:443')
            
            # Test non-IP addresses
            assert not connection.is_websocket_connection('/dev/ttyUSB0')
            assert not connection.is_websocket_connection('COM1')
            assert not connection.is_websocket_connection('example.com')
            assert not connection.is_websocket_connection('localhost')

    def test_parse_websocket_connection(self):
        """Test WebSocket connection string parsing."""
        with patch('serial.Serial') as mock_serial:
            mock_serial.return_value = Mock()
            connection = CircuitPythonConnection('/dev/ttyUSB0')  # Any connection will do
            
            # Test with port
            host, port = connection.parse_websocket_connection('192.168.1.100:8080')
            assert host == '192.168.1.100'
            assert port == 8080
            
            # Test without port (default to 80)
            host, port = connection.parse_websocket_connection('192.168.1.100')
            assert host == '192.168.1.100'
            assert port == 80 