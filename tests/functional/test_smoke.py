#!/usr/bin/env python3
"""
Functional smoke tests for all command files in commands/.
"""

import ast
import json
from pathlib import Path
import pytest

COMMANDS_DIR = Path(__file__).parent.parent.parent / "circremote" / "commands"

# Collect all code.py, info.json, and requirements.txt files
code_py_files = sorted(COMMANDS_DIR.glob("*/code.py"))
info_json_files = sorted(COMMANDS_DIR.glob("*/info.json"))
requirements_files = sorted(COMMANDS_DIR.glob("*/requirements.txt"))

@pytest.mark.parametrize("file_path", code_py_files, ids=lambda p: p.parent.name)
def test_code_py_syntax(file_path):
    """Test that code.py files are valid Python syntax."""
    try:
        content = file_path.read_text(encoding="utf-8")
        ast.parse(content)
    except SyntaxError as e:
        pytest.fail(f"Syntax error in {file_path}: {e}")
    except Exception as e:
        pytest.fail(f"Error reading {file_path}: {e}")

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
    """Test that requirements.txt files are syntactically valid (no empty non-comment lines)."""
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        pytest.fail(f"Error reading {file_path}: {e}")
    lines = content.splitlines()
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if line and not line.startswith('#'):
            if not line:
                pytest.fail(f"Line {i}: Empty non-comment line in {file_path}") 