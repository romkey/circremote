---
name: Command Issue
about: Report problems with specific circremote commands or sensors
labels: ["command", "bug"]
assignees: ["romkey"]
---

## Command Issue Report

### CircuitPython Device Information
- **Board Model**: [e.g., Adafruit MatrixPortal S3, Raspberry Pi Pico, ESP32-S3-DevKitC-1]
- **CircuitPython Version**: [e.g., 9.2.8, 8.2.10]
- **Connection Method**: [e.g., USB Serial, WebSocket, WiFi]

### Command Information
- **Command Name**: [e.g., BME280, ADXL345, custom-sensor]
- **Command Type**: [Built-in, Custom, Remote URL, Pathname]
- **Command Location**: [e.g., Built-in, ~/.circremote/commands/, https://github.com/user/repo/]
- **Full Command Line**: [e.g., `circremote /dev/ttyUSB0 BME280 sda=board.IO1 scl=board.IO2`]

### Hardware Setup
- **Sensor/Module**: [e.g., BME280 Temperature Sensor, ADXL345 Accelerometer]
- **Connection Type**: [e.g., I2C, SPI, UART, GPIO]
- **Wiring Details**: [e.g., SDA=GPIO1, SCL=GPIO2, VCC=3.3V, GND=GND]
- **Power Supply**: [e.g., 3.3V from board, External 5V, etc.]
- **Additional Hardware**: [e.g., Level shifters, Pull-up resistors, etc.]

### Issue Details
- **Error Occurrence**: [e.g., During initialization, During reading, During execution]
- **Error Type**: [e.g., Import error, I2C error, Sensor not found, Runtime error]

### Error Information
**Full error message or traceback:**
```
[Paste the complete error message here]
```

**Steps to reproduce:**
1. [Step 1]
2. [Step 2]
3. [Step 3]
4. [See error]

### Expected Behavior
[Describe what you expected the command to do]

### Actual Behavior
[Describe what actually happened]

### Command Output
**circremote verbose output:**
```
[Paste the complete circremote -v output here]
```

**Device output:**
```
[Paste the output from the device when running the command]
```

**Command file content** (if custom command):
```python
[Paste the code.py content if it's a custom command]
```

**Info.json content** (if available):
```json
[Paste the info.json content if available]
```

### Sensor/Module Verification
- **Hardware Tested**: [Yes/No - Have you tested this sensor with other code?]
- **Alternative Code**: [Yes/No - Does the sensor work with other CircuitPython examples?]
- **Multimeter Readings**: [If applicable, voltage readings at sensor pins]
- **Oscilloscope**: [If applicable, signal quality measurements]

### Dependencies
- **Required Libraries**: [e.g., adafruit_bme680, adafruit_bus_device]
- **Library Versions**: [e.g., adafruit_bme680==1.1.8]
- **Installation Method**: [e.g., circup, manual copy, bundle]
- **Installation Status**: [e.g., Successfully installed, Failed to install, Not attempted]

### Troubleshooting Attempted
- [ ] Verified sensor wiring
- [ ] Checked power supply voltage
- [ ] Tested with known working code
- [ ] Verified I2C/SPI address
- [ ] Checked for conflicting devices
- [ ] Verified library installation
- [ ] Tested with different pins
- [ ] Checked for loose connections

### Additional Context
- **Environment**: [e.g., Indoor, Outdoor, High temperature, High humidity]
- **Previous Working State**: [When did this last work?]
- **Recent Changes**: [Any recent changes to hardware, wiring, or software]
- **Similar Commands**: [Do other similar commands work?]

### Hardware Photos
[If possible, include photos of the wiring setup and connections]

### Additional Notes
[Any other information that might be helpful] 