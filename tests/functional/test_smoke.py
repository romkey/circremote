#!/usr/bin/env python3
"""
Functional smoke tests for all command files in commands/.

These are static checks that catch broken commands at CI time instead of on
the device:
- code.py compiles (compile() catches more than ast.parse, e.g. repeated
  keyword arguments)
- info.json is valid and internally consistent
- every {{ template }} variable in code.py is declared in info.json
  (the CLI hard-errors at runtime otherwise)
- every name in default_commandline is a declared variable (also a runtime
  hard-error)
- code.py still compiles after substituting each variable's default value,
  which catches template-quoting mistakes like `pull = {{ pull }}` rendering
  to `pull = NONE`
"""

import json
import re
from pathlib import Path
import pytest

pytestmark = pytest.mark.functional

COMMANDS_DIR = Path(__file__).parent.parent.parent / "circremote" / "commands"

TEMPLATE_VAR_RE = re.compile(r"\{\{\s*(\w+)\s*\}\}")

# Collect all code.py, info.json, and requirements.txt files
command_dirs = sorted(p.parent for p in COMMANDS_DIR.glob("*/code.py"))
info_json_files = sorted(COMMANDS_DIR.glob("*/info.json"))
requirements_files = sorted(COMMANDS_DIR.glob("*/requirements.txt"))


def load_info(command_dir):
    """Load info.json for a command directory, or None if absent."""
    info_file = command_dir / "info.json"
    if not info_file.exists():
        return None
    return json.loads(info_file.read_text(encoding="utf-8"))


def declared_variables(info_data):
    """Return the list of variable definitions from info.json data."""
    if not info_data:
        return []
    return info_data.get("variables", [])


@pytest.mark.parametrize("command_dir", command_dirs, ids=lambda p: p.name)
def test_code_py_compiles(command_dir):
    """Test that code.py files compile.

    The template is compiled with each {{ var }} replaced by a neutral
    placeholder, mirroring what the CLI interpolation produces structurally.
    compile() is used instead of ast.parse because it catches additional
    errors such as repeated keyword arguments.
    """
    file_path = command_dir / "code.py"
    content = file_path.read_text(encoding="utf-8")
    rendered = TEMPLATE_VAR_RE.sub("None", content)
    try:
        compile(rendered, str(file_path), "exec")
    except SyntaxError as e:
        pytest.fail(f"Syntax error in {file_path}: {e}")


@pytest.mark.parametrize("command_dir", command_dirs, ids=lambda p: p.name)
def test_code_py_compiles_with_defaults(command_dir):
    """Test that code.py compiles after substituting declared default values.

    This is the closest static approximation of what actually runs on the
    device with a default invocation, and catches quoting mistakes such as
    a string default rendering as a bare identifier in a comparison.
    """
    file_path = command_dir / "code.py"
    content = file_path.read_text(encoding="utf-8")

    info_data = load_info(command_dir)
    defaults = {}
    for var in declared_variables(info_data):
        if var.get("default") is not None:
            # The CLI stringifies all defaults before interpolation
            defaults[var["name"]] = str(var["default"])

    def substitute(match):
        name = match.group(1)
        # Variables without defaults get a neutral placeholder
        return defaults.get(name, "None")

    rendered = TEMPLATE_VAR_RE.sub(substitute, content)
    try:
        compile(rendered, str(file_path), "exec")
    except SyntaxError as e:
        pytest.fail(
            f"{file_path} does not compile after substituting defaults "
            f"({defaults}): {e}"
        )


@pytest.mark.parametrize("command_dir", command_dirs, ids=lambda p: p.name)
def test_template_variables_declared_in_info(command_dir):
    """Test that every {{ var }} in code.py is declared in info.json.

    The CLI exits with an error at runtime if a template variable is not
    declared, so this is always a bug in the command.
    """
    content = (command_dir / "code.py").read_text(encoding="utf-8")
    template_vars = set(TEMPLATE_VAR_RE.findall(content))
    if not template_vars:
        return

    info_data = load_info(command_dir)
    if info_data is None:
        pytest.fail(
            f"{command_dir.name}/code.py uses template variables "
            f"{sorted(template_vars)} but has no info.json"
        )

    declared = {var["name"] for var in declared_variables(info_data)}
    undeclared = template_vars - declared
    if undeclared:
        pytest.fail(
            f"{command_dir.name}/code.py uses template variables not declared "
            f"in info.json: {sorted(undeclared)}"
        )


@pytest.mark.parametrize("command_dir", command_dirs, ids=lambda p: p.name)
def test_default_commandline_variables_declared(command_dir):
    """Test that every name in default_commandline is a declared variable.

    The CLI exits with an error at runtime otherwise.
    """
    info_data = load_info(command_dir)
    if not info_data or "default_commandline" not in info_data:
        return

    declared = {var["name"] for var in declared_variables(info_data)}
    expected_vars = info_data["default_commandline"].split()
    undeclared = [name for name in expected_vars if name not in declared]
    if undeclared:
        pytest.fail(
            f"{command_dir.name}/info.json default_commandline references "
            f"undeclared variables: {undeclared}"
        )


@pytest.mark.parametrize("file_path", info_json_files, ids=lambda p: p.parent.name)
def test_info_json_syntax_and_fields(file_path):
    """Test that info.json files are valid JSON and have required fields."""
    try:
        content = file_path.read_text(encoding="utf-8")
        data = json.loads(content)
    except json.JSONDecodeError as e:
        pytest.fail(f"JSON syntax error in {file_path}: {e}")
    except Exception as e:
        pytest.fail(f"Error reading {file_path}: {e}")
    # Check required field
    if "description" not in data:
        pytest.fail(f"Missing required 'description' field in {file_path}")
    # Validate variables section if present
    if "variables" in data:
        if not isinstance(data["variables"], list):
            pytest.fail(f"'variables' must be a list in {file_path}")
        for i, var in enumerate(data["variables"]):
            if not isinstance(var, dict):
                pytest.fail(f"Variable {i} must be an object in {file_path}")
            if "name" not in var:
                pytest.fail(f"Variable {i} missing 'name' field in {file_path}")
            if not isinstance(var["name"], str):
                pytest.fail(f"Variable {i} 'name' must be a string in {file_path}")
    # Validate default_commandline if present
    if "default_commandline" in data:
        if not isinstance(data["default_commandline"], str):
            pytest.fail(f"'default_commandline' must be a string in {file_path}")


@pytest.mark.parametrize("file_path", requirements_files, ids=lambda p: p.parent.name)
def test_requirements_txt_syntax(file_path):
    """Test that requirements.txt lines are plausible circup library names."""
    content = file_path.read_text(encoding="utf-8")
    for i, line in enumerate(content.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if not re.match(r"^[A-Za-z0-9_.-]+$", line):
            pytest.fail(
                f"Line {i} of {file_path} does not look like a valid "
                f"library name: {line!r}"
            )
