"""
Integration tests for end-to-end command execution.

These tests drive CLI.run() with real command directories on disk and a
mocked CircuitPythonConnection, then assert on the interpolated code that
would be sent to the device. This covers the composition of positional
argument parsing, explicit var=value parsing, defaults precedence, device
resolution, and template interpolation.
"""

import json
from unittest.mock import Mock, patch

import pytest

from circremote.cli import CLI

pytestmark = pytest.mark.integration


SAMPLE_CODE = "pin = {{ pin }}\n" "count = {{ count }}\n" 'label = "{{ label }}"\n'

SAMPLE_INFO = {
    "description": "Test command",
    "variables": [
        {"name": "pin", "required": True, "description": "a pin"},
        {"name": "count", "required": False, "description": "a count", "default": 1},
        {
            "name": "label",
            "required": False,
            "description": "a label",
            "default": "default-label",
        },
    ],
    "default_commandline": "pin count label",
    "tested": True,
    "warn_offline": False,
}


@pytest.fixture
def command_dir(tmp_path):
    """Create a command directory with code.py and info.json."""
    cmd_dir = tmp_path / "testcmd"
    cmd_dir.mkdir()
    (cmd_dir / "code.py").write_text(SAMPLE_CODE)
    (cmd_dir / "info.json").write_text(json.dumps(SAMPLE_INFO))
    return cmd_dir


@pytest.fixture
def config_file(tmp_path):
    """Create an isolated (empty) circremote config file."""
    path = tmp_path / "config.json"
    path.write_text(json.dumps({}))
    return path


def run_cli(argv, config_file):
    """Run the CLI with a mocked connection; return the mock connection.

    The -C option isolates the run from the user's real ~/.circremote
    config. time.sleep and monitor_output are patched out for speed. The
    connection's read_available is scripted with the device responses the
    REPL handshake verifies: the normal '>>>' prompt, the raw REPL banner
    and prompt, then the raw REPL 'OK' execution acknowledgment.
    """
    with patch("circremote.cli.CircuitPythonConnection") as mock_conn_class, patch(
        "circremote.cli.time.sleep"
    ), patch.object(CLI, "monitor_output"):
        mock_conn = Mock()
        mock_conn.connection_type = "serial"
        responses = iter([">>> ", "raw REPL; CTRL-B to exit\r\n>", "OK"])
        mock_conn.read_available = Mock(side_effect=lambda *a, **k: next(responses, ""))
        mock_conn_class.return_value = mock_conn

        cli = CLI()
        cli.run(["-C", str(config_file)] + argv)

    return mock_conn


def sent_code(mock_conn):
    """Extract the interpolated program sent to the device.

    run() performs a verified handshake (Ctrl+C/Ctrl+B/newline until '>>>',
    Ctrl+A until the raw REPL banner), then writes the start marker, the
    code, the end marker, Ctrl+D, and finally Ctrl+B.
    """
    writes = [call.args[0] for call in mock_conn.write.call_args_list]
    assert writes[0] == "\x03"  # the handshake begins with an interrupt
    assert "\x01" in writes  # raw REPL mode was requested
    start_index = next(
        i for i, w in enumerate(writes) if w.startswith("print('***START***')")
    )
    assert writes[start_index + 2].startswith("print('***END***')")
    assert writes[start_index + 3] == "\x04"
    assert writes[start_index + 4] == "\x02"
    return writes[start_index + 1].replace("\r\n", "\n")


class TestVariablePipeline:
    """End-to-end tests of argument parsing, defaults, and interpolation."""

    def test_all_positional_arguments(self, command_dir, config_file):
        conn = run_cli(
            ["/dev/ttyUSB0", str(command_dir), "board.D5", "10", "hello"], config_file
        )
        code = sent_code(conn)
        assert "pin = board.D5\n" in code
        assert "count = 10\n" in code
        assert 'label = "hello"\n' in code

    def test_partial_positional_arguments_use_defaults(self, command_dir, config_file):
        conn = run_cli(["/dev/ttyUSB0", str(command_dir), "board.D5"], config_file)
        code = sent_code(conn)
        assert "pin = board.D5\n" in code
        assert "count = 1\n" in code
        assert 'label = "default-label"\n' in code

    def test_explicit_assignments_only(self, command_dir, config_file):
        conn = run_cli(
            ["/dev/ttyUSB0", str(command_dir), "pin=board.D6", "label=custom"],
            config_file,
        )
        code = sent_code(conn)
        assert "pin = board.D6\n" in code
        assert "count = 1\n" in code
        assert 'label = "custom"\n' in code

    def test_mixed_positional_and_explicit(self, command_dir, config_file):
        conn = run_cli(
            ["/dev/ttyUSB0", str(command_dir), "board.D7", "label=mixed"],
            config_file,
        )
        code = sent_code(conn)
        assert "pin = board.D7\n" in code
        assert "count = 1\n" in code
        assert 'label = "mixed"\n' in code

    def test_explicit_assignment_overrides_positional(self, command_dir, config_file):
        conn = run_cli(
            [
                "/dev/ttyUSB0",
                str(command_dir),
                "board.D7",
                "5",
                "pos-label",
                "label=explicit-wins",
            ],
            config_file,
        )
        code = sent_code(conn)
        assert "pin = board.D7\n" in code
        assert "count = 5\n" in code
        assert 'label = "explicit-wins"\n' in code

    def test_quoted_values_are_stripped(self, command_dir, config_file):
        conn = run_cli(
            ["/dev/ttyUSB0", str(command_dir), "pin=board.D5", 'label="quoted"'],
            config_file,
        )
        code = sent_code(conn)
        assert 'label = "quoted"\n' in code

    def test_too_many_positional_arguments_errors(
        self, command_dir, config_file, capsys
    ):
        with pytest.raises(SystemExit):
            run_cli(
                ["/dev/ttyUSB0", str(command_dir), "board.D5", "10", "hello", "extra"],
                config_file,
            )
        captured = capsys.readouterr()
        assert "Too many positional arguments" in captured.out


class TestDeviceDefaults:
    """End-to-end tests of device and global defaults from config."""

    @pytest.fixture
    def device_config_file(self, tmp_path):
        path = tmp_path / "config.json"
        path.write_text(
            json.dumps(
                {
                    "devices": [
                        {
                            "name": "bling",
                            "device": "/dev/ttyUSB9",
                            "defaults": {"pin": "board.MATRIX_DATA", "count": 320},
                        }
                    ],
                    "variable_defaults": {"label": "global-label"},
                }
            )
        )
        return path

    def test_device_defaults_by_name(self, command_dir, device_config_file):
        conn = run_cli(["bling", str(command_dir)], device_config_file)
        code = sent_code(conn)
        assert "pin = board.MATRIX_DATA\n" in code
        assert "count = 320\n" in code

    def test_device_defaults_by_raw_path(self, command_dir, device_config_file):
        conn = run_cli(["/dev/ttyUSB9", str(command_dir)], device_config_file)
        code = sent_code(conn)
        assert "pin = board.MATRIX_DATA\n" in code
        assert "count = 320\n" in code

    def test_global_variable_defaults_apply(self, command_dir, device_config_file):
        conn = run_cli(["bling", str(command_dir)], device_config_file)
        code = sent_code(conn)
        assert 'label = "global-label"\n' in code

    def test_command_line_overrides_device_defaults(
        self, command_dir, device_config_file
    ):
        conn = run_cli(["bling", str(command_dir), "pin=board.D1"], device_config_file)
        code = sent_code(conn)
        assert "pin = board.D1\n" in code
        assert "count = 320\n" in code


class TestBooleanAndNumericDefaults:
    """Defaults declared as JSON types must render usably in Python code."""

    def test_boolean_default_renders_as_python_literal(self, tmp_path, config_file):
        cmd_dir = tmp_path / "boolcmd"
        cmd_dir.mkdir()
        (cmd_dir / "code.py").write_text(
            'flag = "{{ flag }}".lower() in ("true", "1", "yes", "on")\n'
        )
        (cmd_dir / "info.json").write_text(
            json.dumps(
                {
                    "description": "bool test",
                    "variables": [
                        {"name": "flag", "required": False, "default": False},
                    ],
                    "tested": True,
                }
            )
        )

        conn = run_cli(["/dev/ttyUSB0", str(cmd_dir)], config_file)
        code = sent_code(conn)
        # JSON false becomes Python's str(False) == "False"
        assert 'flag = "False".lower()' in code
        # And the rendered code must actually be valid Python
        compile(code, "code.py", "exec")


class TestPlainPythonFile:
    """Commands can also be bare .py files with no info.json."""

    def test_python_file_without_templates(self, tmp_path, config_file):
        py_file = tmp_path / "simple.py"
        py_file.write_text('print("hello from file")\n')

        conn = run_cli(["/dev/ttyUSB0", str(py_file)], config_file)
        code = sent_code(conn)
        assert 'print("hello from file")' in code
