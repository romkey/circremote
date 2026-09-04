"""
Unit tests for the CircuitPythonConnection class.
"""

import base64
from unittest.mock import Mock, patch

import pytest
import serial

from circremote.connection import CircuitPythonConnection

pytestmark = pytest.mark.unit


def make_ws_connection(
    connection_string, password=None, debug_options=None, error=None
):
    """Create a CircuitPythonConnection over a fake WebSocketApp.

    The fake constructor captures the URL, headers, and callbacks, then
    immediately signals either a successful open or the given error, so no
    real network or threads are involved.
    """
    captured = {}

    def fake_wsapp(
        url, header=None, on_open=None, on_message=None, on_error=None, on_close=None
    ):
        ws = Mock()
        captured["url"] = url
        captured["header"] = header
        captured["on_message"] = on_message
        captured["on_close"] = on_close
        captured["ws"] = ws
        if error is not None:
            on_error(ws, error)
        else:
            on_open(ws)
        return ws

    with patch(
        "circremote.connection.websocket.WebSocketApp", side_effect=fake_wsapp
    ), patch("circremote.connection.threading.Thread") as mock_thread:
        captured["thread_cls"] = mock_thread
        conn = CircuitPythonConnection(
            connection_string, password=password, debug_options=debug_options
        )

    return conn, captured


class TestCircuitPythonConnection:
    """Test the CircuitPythonConnection class."""

    def test_init_serial_connection(self):
        """Test initialization of serial connection."""
        with patch("serial.Serial") as mock_serial:
            mock_serial.return_value = Mock()

            connection = CircuitPythonConnection("/dev/ttyUSB0")

            assert connection.connection_type == "serial"
            mock_serial.assert_called_once_with(
                port="/dev/ttyUSB0",
                baudrate=115200,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1,
            )

    def test_init_websocket_connection(self):
        """Test initialization of WebSocket connection."""
        connection, captured = make_ws_connection("192.168.1.100:8080")

        assert connection.connection_type == "websocket"
        assert captured["url"] == "ws://192.168.1.100:8080/cp/serial/"
        assert captured["header"] == {}
        # The WebSocket loop runs in a daemon thread
        captured["thread_cls"].assert_called_once()
        captured["thread_cls"].return_value.start.assert_called_once()

    def test_init_websocket_connection_with_password(self):
        """Test initialization of WebSocket connection with password."""
        connection, captured = make_ws_connection(
            "192.168.1.100:8080", password="secret"
        )

        expected_auth = base64.b64encode(b":secret").decode()
        assert captured["header"] == {"Authorization": f"Basic {expected_auth}"}

    def test_write_serial(self):
        """Test writing to serial connection."""
        with patch("serial.Serial") as mock_serial:
            mock_serial_instance = Mock()
            mock_serial.return_value = mock_serial_instance

            connection = CircuitPythonConnection("/dev/ttyUSB0")
            connection.write("test data")

            mock_serial_instance.write.assert_called_once_with(b"test data")

    def test_write_websocket(self):
        """Test writing to WebSocket connection."""
        connection, captured = make_ws_connection("192.168.1.100:8080")

        connection.write("test data")

        captured["ws"].send.assert_called_once_with("test data")

    def test_read_nonblock_serial(self):
        """Test reading from serial connection."""
        with patch("serial.Serial") as mock_serial:
            mock_serial_instance = Mock()
            mock_serial_instance.read.return_value = b"test data"
            mock_serial.return_value = mock_serial_instance

            connection = CircuitPythonConnection("/dev/ttyUSB0")
            result = connection.read_nonblock(1024)

            assert result == "test data"
            mock_serial_instance.read.assert_called_once_with(1024)

    def test_read_nonblock_serial_no_data(self):
        """Test reading from serial when no data is available."""
        with patch("serial.Serial") as mock_serial:
            mock_serial_instance = Mock()
            mock_serial_instance.read.return_value = b""
            mock_serial.return_value = mock_serial_instance

            connection = CircuitPythonConnection("/dev/ttyUSB0")
            result = connection.read_nonblock(1024)

            assert result == ""
            mock_serial_instance.read.assert_called_once_with(1024)

    def test_read_nonblock_websocket_raises_error(self):
        """Test that read_nonblock raises error for WebSocket connections."""
        connection, captured = make_ws_connection("192.168.1.100:8080")

        with pytest.raises(RuntimeError, match="read_nonblock not supported"):
            connection.read_nonblock(1024)

    def test_read_available_serial_with_waiting_data(self):
        """Test read_available drains buffered serial data."""
        with patch("serial.Serial") as mock_serial:
            mock_serial_instance = Mock()
            mock_serial_instance.in_waiting = 9
            mock_serial_instance.read.return_value = b"test data"
            mock_serial.return_value = mock_serial_instance

            connection = CircuitPythonConnection("/dev/ttyUSB0")
            result = connection.read_available(1024)

            assert result == "test data"
            mock_serial_instance.read.assert_called_once_with(9)

    def test_read_available_serial_no_data(self):
        """Test read_available returns empty string when nothing arrives."""
        with patch("serial.Serial") as mock_serial:
            mock_serial_instance = Mock()
            mock_serial_instance.in_waiting = 0
            mock_serial_instance.read.return_value = b""
            mock_serial.return_value = mock_serial_instance

            connection = CircuitPythonConnection("/dev/ttyUSB0")
            result = connection.read_available(1024)

            assert result == ""
            mock_serial_instance.read.assert_called_once_with(1)

    def test_read_available_websocket_drains_buffer(self):
        """Test that WebSocket messages are buffered and drained in order."""
        connection, captured = make_ws_connection("192.168.1.100:8080")

        captured["on_message"](captured["ws"], "hello ")
        captured["on_message"](captured["ws"], "world")

        assert connection.read_available() == "hello world"
        # Buffer is consumed by the read
        assert connection.read_available() == ""

    def test_flush_serial(self):
        """Test flushing serial connection."""
        with patch("serial.Serial") as mock_serial:
            mock_serial_instance = Mock()
            mock_serial.return_value = mock_serial_instance

            connection = CircuitPythonConnection("/dev/ttyUSB0")
            connection.flush()

            mock_serial_instance.flush.assert_called_once()

    def test_flush_websocket(self):
        """Test that flushing a WebSocket connection is a harmless no-op."""
        connection, captured = make_ws_connection("192.168.1.100:8080")

        connection.flush()

        captured["ws"].flush.assert_not_called()

    def test_close_serial(self):
        """Test closing serial connection."""
        with patch("serial.Serial") as mock_serial:
            mock_serial_instance = Mock()
            mock_serial.return_value = mock_serial_instance

            connection = CircuitPythonConnection("/dev/ttyUSB0")
            connection.close()

            mock_serial_instance.close.assert_called_once()

    def test_close_websocket(self):
        """Test closing WebSocket connection."""
        connection, captured = make_ws_connection("192.168.1.100:8080")

        connection.close()

        captured["ws"].close.assert_called_once()

    def test_on_message_websocket(self):
        """Test that registered message handlers receive WebSocket messages."""
        connection, captured = make_ws_connection("192.168.1.100:8080")

        received = []
        connection.on_message(received.append)

        # Simulate an incoming message from the WebSocket thread
        captured["on_message"](captured["ws"], "hello from device")

        assert received == ["hello from device"]

    def test_on_message_handler_error_does_not_propagate(self):
        """Test that an exception in one handler doesn't break dispatch."""
        connection, captured = make_ws_connection("192.168.1.100:8080")

        received = []

        def bad_handler(msg):
            raise ValueError("handler bug")

        connection.on_message(bad_handler)
        connection.on_message(received.append)

        captured["on_message"](captured["ws"], "still delivered")

        assert received == ["still delivered"]

    def test_on_message_serial_raises_error(self):
        """Test that on_message raises error for serial connections."""
        with patch("serial.Serial") as mock_serial:
            mock_serial_instance = Mock()
            mock_serial.return_value = mock_serial_instance

            connection = CircuitPythonConnection("/dev/ttyUSB0")

            def message_handler(msg):
                pass

            with pytest.raises(
                RuntimeError,
                match="on_message only supported for WebSocket connections",
            ):
                connection.on_message(message_handler)

    def test_connection_error_serial(self):
        """Test handling of serial connection errors."""
        with patch("serial.Serial") as mock_serial:
            mock_serial.side_effect = Exception("Serial connection failed")

            with pytest.raises(Exception, match="Serial connection failed"):
                CircuitPythonConnection("/dev/ttyUSB0")

    def test_connection_error_websocket(self, capsys):
        """Test handling of WebSocket connection-refused errors."""
        with pytest.raises(RuntimeError, match="Connection refused"):
            make_ws_connection(
                "192.168.1.100:8080", error=ConnectionRefusedError("connection refused")
            )

        captured = capsys.readouterr()
        assert "Connection refused" in captured.out
        assert "Web Workflow" in captured.out

    def test_connection_error_websocket_bad_password(self, capsys):
        """Test handling of WebSocket authentication errors."""
        error = Mock()
        error.status_code = 401

        with pytest.raises(RuntimeError, match="Bad password"):
            make_ws_connection("192.168.1.100:8080", password="wrong", error=error)

        captured = capsys.readouterr()
        assert "Bad password" in captured.out
        assert "check your password" in captured.out

    def test_debug_options_serial(self):
        """Test debug options with serial connection."""
        debug_options = Mock()
        debug_options.verbose = True

        with patch("serial.Serial") as mock_serial:
            mock_serial_instance = Mock()
            mock_serial.return_value = mock_serial_instance

            connection = CircuitPythonConnection(
                "/dev/ttyUSB0", debug_options=debug_options
            )

            assert connection.debug_options == debug_options

    def test_debug_options_websocket(self, capsys):
        """Test debug output with WebSocket connection in verbose mode."""
        connection, captured = make_ws_connection(
            "192.168.1.100:8080", debug_options={"verbose": True}
        )

        assert connection.debug_options == {"verbose": True}
        out = capsys.readouterr().out
        assert "Establishing WebSocket connection" in out
        assert "Connected to CircuitPython Web Workflow at 192.168.1.100:8080" in out

    def test_websocket_url_parsing(self):
        """Test WebSocket URL construction, including wss for port 443."""
        connection, captured = make_ws_connection("10.0.0.1")
        assert captured["url"] == "ws://10.0.0.1:80/cp/serial/"

        connection, captured = make_ws_connection("10.0.0.1:443")
        assert captured["url"] == "wss://10.0.0.1:443/cp/serial/"

    def test_websocket_headers_with_password(self):
        """Test WebSocket headers with and without password authentication."""
        _, captured = make_ws_connection("192.168.1.100:8080")
        assert captured["header"] == {}

        _, captured = make_ws_connection("192.168.1.100:8080", password="hunter2")
        auth = captured["header"]["Authorization"]
        assert auth.startswith("Basic ")
        assert base64.b64decode(auth.split()[1]).decode() == ":hunter2"

    def test_is_websocket_connection(self):
        """Test WebSocket connection detection."""
        test_cases = [
            ("192.168.1.100:8080", True),
            ("192.168.1.100", True),
            ("10.0.0.1:443", True),
            ("172.16.0.1", True),
            ("example.com:443", False),  # Hostnames are not supported
            ("example.com", False),  # Hostnames are not supported
            ("/dev/ttyUSB0", False),
            ("COM3", False),
            ("./local_file.py", False),
        ]

        # Create a connection instance to test the method
        with patch("serial.Serial") as mock_serial:
            mock_serial.return_value = Mock()
            connection = CircuitPythonConnection("/dev/ttyUSB0")

            for connection_spec, expected in test_cases:
                result = connection.is_websocket_connection(connection_spec)
                assert (
                    result == expected
                ), f"Expected {expected} for '{connection_spec}', got {result}"

    def test_parse_websocket_connection(self):
        """Test WebSocket connection parsing."""
        test_cases = [
            ("192.168.1.100:8080", ("192.168.1.100", 8080)),
            ("192.168.1.100", ("192.168.1.100", 80)),
            ("example.com:443", ("example.com", 443)),
            ("example.com", ("example.com", 80)),
        ]

        # Create a connection instance to test the method
        with patch("serial.Serial") as mock_serial:
            mock_serial.return_value = Mock()
            connection = CircuitPythonConnection("/dev/ttyUSB0")

            for connection_spec, expected in test_cases:
                host, port = connection.parse_websocket_connection(connection_spec)
                assert (
                    host,
                    port,
                ) == expected, (
                    f"Expected {expected} for '{connection_spec}', got ({host}, {port})"
                )
