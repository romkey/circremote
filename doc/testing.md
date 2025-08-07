# Testing Guide

This document explains how to run tests for the circremote project with improved interruption handling.

## Quick Start

### Recommended: Use the Custom Test Runner
```bash
# Run all tests with graceful interruption handling
python run_tests.py

# Run specific test categories
python run_tests.py tests/unit/
python run_tests.py tests/functional/
python run_tests.py tests/integration/

# Run specific tests
python run_tests.py tests/unit/test_config.py::TestConfig::test_get_circup_path_command_line_precedence
```

### Standard pytest (also improved)
```bash
# Run all tests (quiet mode)
python -m pytest

# Run with verbose output (if needed)
python -m pytest -v

# Run specific test categories
python -m pytest tests/unit/
python -m pytest tests/functional/
python -m pytest tests/integration/
```

## Improvements Made

### 1. Graceful Interruption Handling
- **Before**: Ctrl+C would spew screens of garbage output
- **After**: Clean exit with "Interrupted by user. Exiting gracefully..." message

### 2. Reduced Output Noise
- **Before**: Verbose output by default with lots of details
- **After**: Quiet mode by default, showing only essential information

### 3. Better Test Organization
- Added `--maxfail=10` to stop after 10 failures
- Added `--durations=10` to show slowest 10 tests
- Added `--disable-warnings` to reduce warning noise

## Configuration Files

### pytest.ini
Updated with quieter defaults:
```ini
addopts = 
    --strict-markers
    --strict-config
    --tb=short
    --disable-warnings
    --quiet
    --maxfail=10
    --durations=10
```

### conftest.py
Added signal handlers for graceful interruption:
```python
def pytest_configure(config):
    def signal_handler(signum, frame):
        print("\n\nInterrupted by user. Exiting gracefully...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
```

### run_tests.py
Custom test runner with enhanced interruption handling:
- Wraps pytest in a subprocess
- Handles SIGINT and SIGTERM signals
- Provides clean exit messages
- Passes through all pytest arguments

## Test Categories

- **Unit Tests** (`tests/unit/`): Fast, isolated tests
- **Functional Tests** (`tests/functional/`): End-to-end functionality tests
- **Integration Tests** (`tests/integration/`): System integration tests

## Tips

1. **For development**: Use `python run_tests.py` for the best experience
2. **For debugging**: Use `python -m pytest -v` for verbose output
3. **For CI/CD**: Use `python -m pytest` for standard output
4. **For coverage**: Use `python -m pytest --cov=circremote --cov-report=html`

## Troubleshooting

If you still see verbose output:
1. Check that you're using the updated `pytest.ini`
2. Make sure `conftest.py` is in the root directory
3. Try using `python run_tests.py` instead of `python -m pytest`

If tests hang or don't respond to Ctrl+C:
1. Use `python run_tests.py` which has better signal handling
2. Check for any infinite loops in test code
3. Use `--maxfail=1` to stop on first failure 