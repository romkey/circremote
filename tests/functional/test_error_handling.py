"""
Functional tests for error handling scenarios.

These tests drive CLI.run() with real command directories on disk (via
tmp_path) and a mocked CircuitPythonConnection, asserting that each error
path exits and prints a useful message.
"""

import json
import threading
from unittest.mock import Mock, patch

import pytest

from circremote.cli import CLI
from tests.conftest import make_options

pytestmark = pytest.mark.functional


@pytest.fixture
def config_file(tmp_path):
    """Create an isolated (empty) circremote config file."""
    path = tmp_path / "config.json"
    path.write_text(json.dumps({}))
    return path


def make_command(tmp_path, code="print('hi')\n", info=None, name="errcmd"):
    """Create a command directory with code.py and optional info.json."""
    cmd_dir = tmp_path / name
    cmd_dir.mkdir()
    (cmd_dir / "code.py").write_text(code)
    if info is not None:
        (cmd_dir / "info.json").write_text(
            info if isinstance(info, str) else json.dumps(info)
        )
    return cmd_dir


def run_cli(argv, config_file, connect_error=None):
    """Run the CLI with a mocked connection; return the mock connection.

    read_available is scripted with the device responses the REPL handshake
    verifies: the normal '>>>' prompt, the raw REPL banner and prompt, then
    the raw REPL 'OK' execution acknowledgment.
    """
    with patch("circremote.cli.CircuitPythonConnection") as mock_conn_class, patch(
        "circremote.cli.time.sleep"
    ), patch.object(CLI, "monitor_output"):
        if connect_error is not None:
            mock_conn_class.side_effect = connect_error
        else:
            mock_conn = Mock()
            mock_conn.connection_type = "serial"
            responses = iter([">>> ", "raw REPL; CTRL-B to exit\r\n>", "OK"])
            mock_conn.read_available = Mock(
                side_effect=lambda *a, **k: next(responses, "")
            )
            mock_conn_class.return_value = mock_conn

        cli = CLI()
        cli.run(["-C", str(config_file)] + argv)

    return None if connect_error else mock_conn


class TestErrorHandling:
    """Test error handling in various scenarios."""

    def test_missing_command_directory(self, config_file, capsys):
        """Test error when the command doesn't exist anywhere."""
        with pytest.raises(SystemExit) as exc_info:
            run_cli(["/dev/ttyUSB0", "definitely_not_a_real_command_xyz"], config_file)
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert (
            "Error: Command 'definitely_not_a_real_command_xyz' not found"
            in captured.out
        )
        assert "Available commands:" in captured.out

    def test_missing_pathname_directory(self, config_file, capsys):
        """Test error when an explicit pathname command doesn't exist."""
        with pytest.raises(SystemExit) as exc_info:
            run_cli(["/dev/ttyUSB0", "/nonexistent/path/to/command"], config_file)
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "does not exist" in captured.out

    def test_missing_code_py(self, tmp_path, config_file, capsys):
        """Test error when code.py doesn't exist in command directory."""
        cmd_dir = tmp_path / "no_code"
        cmd_dir.mkdir()
        (cmd_dir / "info.json").write_text(json.dumps({"description": "no code here"}))

        with pytest.raises(SystemExit) as exc_info:
            run_cli(["/dev/ttyUSB0", str(cmd_dir)], config_file)
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "code.py not found" in captured.out

    def test_invalid_variables(self, tmp_path, config_file, capsys):
        """Test error when undeclared variables are provided."""
        cmd_dir = make_command(
            tmp_path,
            code="pin = {{ pin }}\n",
            info={
                "description": "test",
                "variables": [{"name": "pin", "required": True}],
                "tested": True,
            },
        )

        with pytest.raises(SystemExit) as exc_info:
            run_cli(
                ["/dev/ttyUSB0", str(cmd_dir), "pin=board.D1", "bogus=1"], config_file
            )
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Invalid variables" in captured.out
        assert "'bogus' is not a valid variable" in captured.out

    def test_missing_template_variables(self, tmp_path, config_file, capsys):
        """Test error when a template variable gets no value from anywhere."""
        cmd_dir = make_command(
            tmp_path,
            code="pin = {{ pin }}\nother = {{ other }}\n",
            info={
                "description": "test",
                "variables": [
                    {"name": "pin", "required": True},
                    {"name": "other", "required": True},
                ],
                "tested": True,
            },
        )

        # Provide only one of the two required variables
        with pytest.raises(SystemExit) as exc_info:
            run_cli(["/dev/ttyUSB0", str(cmd_dir), "pin=board.D1"], config_file)
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "not provided on command line" in captured.out
        assert "'{{ other }}' requires a value" in captured.out

    def test_no_variables_at_all(self, tmp_path, config_file, capsys):
        """Test error when code has templates but nothing supplies any value."""
        cmd_dir = make_command(
            tmp_path,
            code="pin = {{ pin }}\n",
            info={
                "description": "test",
                "variables": [{"name": "pin", "required": True}],
                "tested": True,
            },
        )

        with pytest.raises(SystemExit) as exc_info:
            run_cli(["/dev/ttyUSB0", str(cmd_dir)], config_file)
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "no variables available" in captured.out
        assert "'{{ pin }}' requires a value" in captured.out

    def test_undeclared_template_variable(self, tmp_path, config_file, capsys):
        """Test error when code.py uses a template var not in info.json."""
        cmd_dir = make_command(
            tmp_path,
            code="pin = {{ pin }}\nmystery = {{ mystery }}\n",
            info={
                "description": "test",
                "variables": [{"name": "pin", "required": True}],
                "tested": True,
            },
        )

        with pytest.raises(SystemExit) as exc_info:
            run_cli(["/dev/ttyUSB0", str(cmd_dir), "pin=board.D1"], config_file)
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "not defined in info.json" in captured.out
        assert "'{{ mystery }}' is not a valid variable" in captured.out

    def test_connection_error(self, tmp_path, config_file, capsys):
        """Test error when the connection cannot be established."""
        cmd_dir = make_command(tmp_path, info={"description": "test", "tested": True})

        with pytest.raises(SystemExit) as exc_info:
            run_cli(
                ["/dev/ttyUSB0", str(cmd_dir)],
                config_file,
                connect_error=RuntimeError("serial port on fire"),
            )
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error establishing connection: serial port on fire" in captured.out

    def test_connection_refused_exits_quietly(self, tmp_path, config_file, capsys):
        """Test that connection-refused errors exit without a duplicate message."""
        cmd_dir = make_command(tmp_path, info={"description": "test", "tested": True})

        with pytest.raises(SystemExit) as exc_info:
            run_cli(
                ["/dev/ttyUSB0", str(cmd_dir)],
                config_file,
                connect_error=ConnectionRefusedError("Connection refused"),
            )
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        # connection.py already printed details; run() must not add another error
        assert "Error establishing connection" not in captured.out

    def test_invalid_json_in_info(self, tmp_path, config_file, capsys):
        """Test warning (not error) when info.json has invalid JSON."""
        cmd_dir = make_command(tmp_path, info="{ this is not json !!!")

        conn = run_cli(["/dev/ttyUSB0", str(cmd_dir)], config_file)
        captured = capsys.readouterr()
        assert "Warning: Could not parse info.json" in captured.out
        assert "Proceeding without module information" in captured.out
        # The command still runs
        assert conn.write.called

    def test_missing_info_json(self, tmp_path, config_file, capsys):
        """Test warning when info.json is absent entirely."""
        cmd_dir = make_command(tmp_path, info=None)

        conn = run_cli(["/dev/ttyUSB0", str(cmd_dir)], config_file)
        captured = capsys.readouterr()
        assert "Warning: info.json not found" in captured.out
        assert conn.write.called

    def test_missing_description_in_info(self, tmp_path, config_file, capsys):
        """Test that a missing description just skips the module banner."""
        cmd_dir = make_command(tmp_path, info={"tested": True})

        conn = run_cli(["/dev/ttyUSB0", str(cmd_dir)], config_file)
        captured = capsys.readouterr()
        assert "Description:" not in captured.out
        assert conn.write.called

    def test_too_many_positional_arguments(self, tmp_path, config_file, capsys):
        """Test error when too many positional arguments are provided."""
        cmd_dir = make_command(
            tmp_path,
            code="pin = {{ pin }}\n",
            info={
                "description": "test",
                "variables": [{"name": "pin", "required": True}],
                "default_commandline": "pin",
                "tested": True,
            },
        )

        with pytest.raises(SystemExit) as exc_info:
            run_cli(["/dev/ttyUSB0", str(cmd_dir), "board.D1", "extra"], config_file)
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Too many positional arguments" in captured.out
        assert "Expected at most 1 arguments" in captured.out

    def test_partial_positional_arguments_succeed(self, tmp_path, config_file):
        """Test that missing positional arguments fall back to defaults."""
        cmd_dir = make_command(
            tmp_path,
            code="pin = {{ pin }}\ncount = {{ count }}\n",
            info={
                "description": "test",
                "variables": [
                    {"name": "pin", "required": True},
                    {"name": "count", "required": False, "default": 3},
                ],
                "default_commandline": "pin count",
                "tested": True,
            },
        )

        conn = run_cli(["/dev/ttyUSB0", str(cmd_dir), "board.D1"], config_file)
        writes = [call.args[0] for call in conn.write.call_args_list]
        # The code is written immediately after the start marker
        start_index = next(
            i for i, w in enumerate(writes) if w.startswith("print('***START***')")
        )
        code = writes[start_index + 1].replace("\r\n", "\n")
        assert "pin = board.D1\n" in code
        assert "count = 3\n" in code

    def test_invalid_default_commandline(self, tmp_path, config_file, capsys):
        """Test error when default_commandline references undeclared variables."""
        cmd_dir = make_command(
            tmp_path,
            code="pin = {{ pin }}\n",
            info={
                "description": "test",
                "variables": [{"name": "pin", "required": True}],
                "default_commandline": "pin nonexistent",
                "tested": True,
            },
        )

        with pytest.raises(SystemExit) as exc_info:
            run_cli(["/dev/ttyUSB0", str(cmd_dir), "board.D1"], config_file)
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "default_commandline" in captured.out
        assert "'nonexistent' is not a valid variable" in captured.out

    def test_untested_command_quiet_without_yes_errors(
        self, tmp_path, config_file, capsys
    ):
        """Test that an untested command in quiet mode without -y exits."""
        cmd_dir = make_command(tmp_path, info={"description": "test", "tested": False})

        with pytest.raises(SystemExit) as exc_info:
            run_cli(["-q", "/dev/ttyUSB0", str(cmd_dir)], config_file)
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "untested" in captured.err

    def test_untested_command_yes_proceeds(self, tmp_path, config_file, capsys):
        """Test that -y bypasses the untested-command confirmation."""
        cmd_dir = make_command(tmp_path, info={"description": "test", "tested": False})

        conn = run_cli(["-y", "/dev/ttyUSB0", str(cmd_dir)], config_file)
        captured = capsys.readouterr()
        assert "Proceeding without confirmation" in captured.out
        assert conn.write.called

    def test_offline_warning_declined_cancels(self, tmp_path, config_file, capsys):
        """Test that declining the offline warning cancels the run."""
        cmd_dir = make_command(
            tmp_path,
            info={"description": "test", "tested": True, "warn_offline": True},
        )

        with patch("builtins.input", return_value="n"):
            with pytest.raises(SystemExit) as exc_info:
                run_cli(["/dev/ttyUSB0", str(cmd_dir)], config_file)
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "Operation cancelled by user" in captured.out


class TestTimeoutHandling:
    """Test timeout wiring in monitor_output without a real connection."""

    def _serial_connection(self):
        conn = Mock()
        conn.connection_type = "serial"
        return conn

    def test_timeout_option_serial_connection(self, cli_instance):
        """Test that a serial connection arms and cancels the timeout."""
        options = make_options(timeout=5.0)
        conn = self._serial_connection()

        with patch("signal.signal") as mock_signal, patch(
            "signal.alarm"
        ) as mock_alarm, patch.object(CLI, "monitor_serial_output") as mock_monitor:
            cli_instance.monitor_output(conn, options)

        mock_signal.assert_called_once()
        # Armed with the configured timeout, then cancelled afterwards
        assert mock_alarm.call_args_list[0].args == (5,)
        assert mock_alarm.call_args_list[-1].args == (0,)
        mock_monitor.assert_called_once()

    def test_timeout_option_websocket_connection(self, cli_instance):
        """Test that WebSocket connections do not arm the serial timeout."""
        options = make_options(timeout=5.0)
        conn = Mock()
        conn.connection_type = "websocket"

        with patch("signal.alarm") as mock_alarm, patch.object(
            CLI, "monitor_websocket_output"
        ) as mock_monitor:
            cli_instance.monitor_output(conn, options)

        mock_alarm.assert_not_called()
        mock_monitor.assert_called_once()

    def test_timeout_zero_wait_indefinitely(self, cli_instance):
        """Test that timeout=0 never arms a timeout."""
        options = make_options(timeout=0)
        conn = self._serial_connection()

        with patch("signal.alarm") as mock_alarm, patch.object(
            CLI, "monitor_serial_output"
        ) as mock_monitor:
            cli_instance.monitor_output(conn, options)

        mock_alarm.assert_not_called()
        mock_monitor.assert_called_once()

    def test_timeout_flag_stops_monitoring(self, cli_instance, default_options):
        """Test that a set timeout flag breaks the serial monitoring loop."""
        conn = self._serial_connection()
        conn.read_available.return_value = ""

        flag = threading.Event()
        flag.set()
        # Must return promptly instead of looping forever
        cli_instance.monitor_serial_output(conn, default_options, flag)

    def test_serial_output_between_markers_is_printed(
        self, cli_instance, default_options, capsys
    ):
        """Test that only content between START/END markers is displayed."""
        conn = self._serial_connection()
        conn.read_available.side_effect = [
            "garbage***START***hello ",
            "world***END***trailing",
        ]

        with patch("circremote.cli.time.sleep"):
            cli_instance.monitor_serial_output(conn, default_options)

        captured = capsys.readouterr()
        assert "hello world" in captured.out
        assert "garbage" not in captured.out
        assert "trailing" not in captured.out
