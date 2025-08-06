---
name: Runtime Issue
about: Report problems running circremote commands
title: "[RUNTIME] "
labels: ["runtime", "bug"]
assignees: ["romkey"]
---

## Runtime Issue Report

### Host System Information
- **Operating System**: [e.g., macOS 14.0, Ubuntu 22.04, Windows 11]
- **Python Version**: [e.g., Python 3.11.5]
- **circremote Version**: [e.g., 1.0.0, git commit hash if from source]

### CircuitPython Device Information
- **Board Model**: [e.g., Adafruit MatrixPortal S3, Raspberry Pi Pico, ESP32-S3-DevKitC-1]
- **CircuitPython Version**: [e.g., 9.2.8, 8.2.10]
- **Connection Method**: [e.g., USB Serial, WebSocket, WiFi]
- **Device Address/Port**: [e.g., /dev/ttyUSB0, 10.0.1.23:8080, COM3]

### Issue Details
- **Command Being Run**: [e.g., `circremote /dev/ttyUSB0 BME280`]
- **Full Command Line**: [e.g., `circremote -v /dev/ttyUSB0 BME280 sda=board.IO1 scl=board.IO2`]
- **Error Occurrence**: [e.g., During connection, during code upload, during execution, during output monitoring]

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
[Describe what you expected to happen when running the command]

### Actual Behavior
[Describe what actually happened]

### Device State
- **Device Boot Status**: [e.g., Normal boot, Safe mode, Recovery mode]
- **Storage Space**: [e.g., 1.2MB free of 2MB total]
- **Connected Sensors/Modules**: [List any connected hardware]
- **Previous Commands**: [Any commands that were run before this issue]

### Connection Details
- **Connection Type**: [Serial/USB/WebSocket/WiFi]
- **Connection Speed** (if serial): [e.g., 115200 baud]
- **Connection Stability**: [e.g., Stable, Intermittent, Unstable]
- **Device Visibility**: [e.g., Shows as CIRCUITPY drive, Shows in device manager, Not visible]

### Logs and Output
**circremote verbose output:**
```
[Paste the complete circremote -v output here]
```

**Device serial output** (if available):
```
[Paste any output from the device itself]
```

**System logs** (if relevant):
```
[Paste relevant system logs like dmesg, lsusb, etc.]
```

### Troubleshooting Attempted
- [ ] Verified device is connected and visible
- [ ] Checked CircuitPython version compatibility
- [ ] Tried different connection methods
- [ ] Restarted the device
- [ ] Checked for conflicting processes
- [ ] Verified network connectivity (if using WebSocket)
- [ ] Checked USB cable/connection (if using USB)

### Additional Context
- **Hardware Setup**: [Description of connected sensors, wiring, etc.]
- **Environment**: [e.g., Development, Production, Testing]
- **Previous Working State**: [When did this last work?]
- **Recent Changes**: [Any recent changes to system, hardware, or software]

### Additional Notes
[Any other information that might be helpful] 