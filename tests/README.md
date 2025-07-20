# circremote-python Test Suite

This directory contains the comprehensive testing infrastructure for circremote-python.

## Directory Structure

```
tests/
├── __init__.py                 # Tests package
├── conftest.py                 # Pytest configuration and fixtures
├── unit/                       # Unit tests
│   ├── __init__.py
│   ├── test_cli.py            # CLI class unit tests
│   ├── test_config.py         # Config class unit tests
│   └── test_connection.py     # Connection class unit tests
├── integration/                # Integration tests
│   ├── __init__.py
│   └── test_command_execution.py  # End-to-end command execution tests
├── functional/                 # Functional tests
│   ├── __init__.py
│   ├── test_smoke.py          # Smoke tests for all command files
│   └── test_error_handling.py # Error handling scenarios
└── fixtures/                   # Test data and fixtures
    ├── sample_commands/        # Sample command files for testing
    ├── mock_devices/           # Mock device configurations
    └── test_configs/           # Test configuration files
```

## Test Categories

### Unit Tests (`tests/unit/`)
- **Purpose**: Test individual functions and classes in isolation
- **Coverage**: CLI parsing, config loading, connection handling, variable interpolation
- **Tools**: pytest, unittest.mock
- **Run**: `pytest tests/unit/`

### Integration Tests (`tests/integration/`)
- **Purpose**: Test how components work together
- **Coverage**: End-to-end command execution, variable parsing, template interpolation
- **Tools**: pytest, mock serial/WebSocket connections
- **Run**: `pytest tests/integration/`

### Functional Tests (`tests/functional/`)
- **Purpose**: Test the software as a complete system
- **Coverage**: All command files, syntax validation, error scenarios
- **Tools**: pytest, current smoke test logic
- **Run**: `pytest tests/functional/`

## Running Tests

### Prerequisites
Install development dependencies:
```bash
pip install -e .[dev]
```

### Run All Tests
```bash
pytest
```

### Run Specific Test Categories
```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Functional tests only
pytest tests/functional/

# Smoke tests only
pytest tests/functional/test_smoke.py
```

### Run with Coverage
```bash
pytest --cov=circremote --cov-report=html --cov-report=term-missing
```

### Run with Tox (Multi-environment)
```bash
# Run all environments
tox

# Run specific environment
tox -e py311

# Run linting
tox -e lint

# Run with coverage
tox -e coverage
```

## Test Markers

Tests are categorized using pytest markers:

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests  
- `@pytest.mark.functional` - Functional tests
- `@pytest.mark.slow` - Slow running tests
- `@pytest.mark.serial` - Tests requiring serial connection
- `@pytest.mark.websocket` - Tests requiring WebSocket connection

Run tests by marker:
```bash
pytest -m unit
pytest -m integration
pytest -m functional
```

## Continuous Integration

The project uses GitHub Actions for automated testing:

- **Python Versions**: 3.7, 3.8, 3.9, 3.10, 3.11
- **Linting**: flake8, black, isort
- **Coverage**: Codecov integration
- **Triggers**: Push to main/develop, pull requests

## Test Fixtures

Common test fixtures are defined in `conftest.py`:

- `commands_dir` - Path to commands directory
- `sample_command_dir` - Sample command directory (BME280)
- `sample_info_json` - Sample info.json data
- `sample_code_py` - Sample code.py content
- `cli_instance` - CLI instance for testing
- `mock_serial_connection` - Mock serial connection
- `mock_websocket_connection` - Mock WebSocket connection
- `temp_command_dir` - Temporary command directory
- `sample_command_files` - Complete sample command files
- `mock_config` - Mock config for testing

## Writing Tests

### Unit Tests
Test individual methods and functions:
```python
def test_parse_command_line_variables(self, cli_instance):
    """Test parsing explicit variable assignments."""
    args = ['sda=board.IO1', 'scl=board.IO2']
    result = cli_instance.parse_command_line_variables(args)
    
    expected = {'sda': 'board.IO1', 'scl': 'board.IO2'}
    assert result == expected
```

### Integration Tests
Test component interactions:
```python
def test_basic_command_execution_flow(self, cli_instance, sample_command_files):
    """Test basic command execution flow with mocked connection."""
    with patch('circremote.cli.CircuitPythonConnection') as mock_conn_class:
        # Mock connection and run command
        # Verify expected interactions
```

### Functional Tests
Test complete workflows:
```python
def test_missing_command_directory(self, cli_instance):
    """Test error when command directory doesn't exist."""
    with pytest.raises(SystemExit):
        cli_instance.run(['/dev/ttyUSB0', 'nonexistent_command'])
```

## Best Practices

1. **Use fixtures** for common test data and setup
2. **Mock external dependencies** (serial, WebSocket, file system)
3. **Test both success and failure scenarios**
4. **Use descriptive test names** that explain what is being tested
5. **Group related tests** in classes
6. **Use appropriate markers** for test categorization
7. **Keep tests fast** by avoiding real hardware connections
8. **Test edge cases** and error conditions

## Adding New Tests

1. **Unit tests**: Add to appropriate `tests/unit/test_*.py` file
2. **Integration tests**: Add to `tests/integration/test_*.py` file
3. **Functional tests**: Add to `tests/functional/test_*.py` file
4. **New test files**: Create new `test_*.py` files as needed
5. **Fixtures**: Add to `conftest.py` if shared across multiple test files

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure you're running from the project root
2. **Mock issues**: Check that mocks are properly configured
3. **Path issues**: Use `Path(__file__).parent` for relative paths
4. **Fixture errors**: Verify fixture names match test parameters

### Debug Mode
Run tests with verbose output:
```bash
pytest -v -s
```

### Test Discovery
Check which tests are discovered:
```bash
pytest --collect-only
``` 