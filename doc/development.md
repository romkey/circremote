## Development

### Installing Locally

```bash
pip install -e .
```

### Running Tests

```bash
# Run all tests (quiet mode with graceful interruption)
python -m pytest

# Run with custom test runner (recommended for better interruption handling)
python run_tests.py

# Run specific test categories
python -m pytest tests/unit/
python -m pytest tests/functional/
python -m pytest tests/integration/

# Run with verbose output (if needed)
python -m pytest -v

# Run with coverage
python -m pytest --cov=circremote --cov-report=html
```
