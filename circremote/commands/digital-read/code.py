# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import digitalio

# Pin configuration
pin = {{ pin }}

print(f"Digital Read")
print(f"Pin: {pin}")

# Initialize digital input
digital_pin = digitalio.DigitalInOut(pin)
digital_pin.direction = digitalio.Direction.INPUT

# Configure pull resistor if specified
pull = "{{ pull }}"
if pull == "UP":
    digital_pin.pull = digitalio.Pull.UP
    print("Pull-up resistor enabled")
elif pull == "DOWN":
    digital_pin.pull = digitalio.Pull.DOWN
    print("Pull-down resistor enabled")
else:
    print("No pull resistor")

def read_digital_value():
    """Read and display digital value from the pin."""
    try:
        # Read digital value
        value = digital_pin.value
        
        print(f"Digital Value: {value}")
        print(f"Logic Level: {'HIGH' if value else 'LOW'}")
        
        # Provide context about the reading
        if value:
            print("Status: Pin is HIGH (3.3V or 5V)")
        else:
            print("Status: Pin is LOW (0V or GND)")
        
        return value
        
    except Exception as e:
        print(f"Error reading digital pin: {e}")
        return None

def continuous_read():
    """Continuously read digital values."""
    print("Starting continuous digital reading...")
    print("Press Ctrl+C to stop")
    print("=" * 40)
    
    try:
        while True:
            value = read_digital_value()
            print("-" * 20)
            time.sleep({{ interval }})
            
    except KeyboardInterrupt:
        print("\nStopping digital read...")
        print("Digital read stopped.")

# Perform the digital read
continuous = "{{ continuous }}".lower() in ("true", "1", "yes", "on")
if continuous:
    continuous_read()
else:
    read_digital_value()

