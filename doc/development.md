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

### Command Structure

Commands consist of three files that are stored in a directory with the name of the command.

- `code.py` - the Python code for the command
- `requirements.txt` - required libraries to be installed by `circup`
- `info.json` - information about the command

#### `code.py`

Just like a `code.py` file that's stored on a CircuitPython device, on this file is never saved to the device's internal flash storage.

Maximum size will depend on the available memory on the device.

##### Variables

The file supports very limited substitutions using the syntax `{{NAME}}` - that string will be replaced with the value of the variable named `NAME`. Variables must be listed in `info.json`. We use double curly braces to try to avoid confusion with f-string substitutions.

For instance:
```
import time
import board
import busio
import adafruit_bme680

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize BME680
try:
    bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, address={{ address }})

```

If suppose `scl` is `board.SCL`, `sda` is `board.SDA` and `address` is `0x76`. The result would be:
```
import time
import board
import busio
import adafruit_bme680

# Initialize I2C with fallback
try:
    i2c = busio.I2C(board.SCL, board.SDA)
except:
    i2c = board.I2C()

# Initialize BME680
try:
    bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=0x76)

```

If `scl` and `sda` are not defined, the result would be:
```
import time
import board
import busio
import adafruit_bme680

# Initialize I2C with fallback
try:
    i2c = busio.I2C()
except:
    i2c = board.I2C()

# Initialize BME680
try:
    bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=0x76)

```

The `busio.I2C()` line would throw an exception and control would pass to the `board.I2C()` line which would use the default I2C pins for the board.

Variables are interpolated using direction string replacement, without any type checking - they're all strings. If you need the result in the Python code to be a string, make sure you include quotes around it in the code.

For instance, if `filename` is `settings.toml` then this code would fail:
```
print({{ filename }}) 
```
and this code would work:
```
print("{{ filename }}")
```

Variables can be optional or required, and can have a default value. Variables with a default value are always optional.

##### Default command line

A command can include a default command line which has variables automatically substituted in it.

For instance, the `cat` command takes one variable, `filename`. It also has a default commandline of `filename`.

You can run it like this:
`circremote DEVICE cat filename=settings.toml`
or like this:
`circremote DEVICE cat settings.toml`
and the filename will automatically be set.

#### `requirements.txt`

Normal file format, one library name per line, comments start with \#

#### `info.json`

This is a JSON file with information about the command. This is an example for the `cat` command:
```
{
  "description": "Output a file",
  "warn_unavailable": false,
  "variables": [
    {
      "name": "filename",
      "required": true,
      "description": "File to cat",
      "default": null
    }
  ],
  "tested": true,
  "default_commandline": "filename"
}
```

- `description` is used by `-h` to describe what the command does
- `warn_unavailable` indicates that the user should be warned that this could make the device unavailable or unreachable
- `variables` - an array of variables, each has a `named, `required` flag, `description and a `default` value
- `tested` - this indicates whether the command has been tested. Many commands were written by an LLM. While they're verified to parse correctly they may not yet have been truly tested with hardware.
- `default_commandline` - this is the default command line, used with variable substitutions

