# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import analogio

# Pin configuration
pin = {{ pin }}

print(f"Analog Read")
print(f"Pin: {pin}")

# Initialize analog input
analog_pin = analogio.AnalogIn(pin)

# ADC full-scale reference (varies by board; do not assume 3.3V)
reference_voltage = analog_pin.reference_voltage

def read_analog_value():
    """Read and display analog value from the pin."""
    try:
        # Read raw ADC value
        raw_value = analog_pin.value
        
        # Read normalized value (0.0-1.0)
        normalized = raw_value / 65535
        
        # Read voltage relative to the ADC reference
        voltage = normalized * reference_voltage
        
        print(f"Raw ADC Value: {raw_value}")
        print(f"Voltage: {voltage:.3f}V (ref {reference_voltage:.2f}V)")
        print(f"Normalized: {normalized:.3f}")
        
        # Provide some context about the reading
        if normalized < 0.05:
            print("Status: Near ground (low)")
        elif normalized > 0.95:
            print("Status: Near reference (high)")
        else:
            print("Status: Intermediate voltage level")
        
        return raw_value, voltage, normalized
        
    except Exception as e:
        print(f"Error reading analog pin: {e}")
        return None, None, None

def continuous_read():
    """Continuously read analog values."""
    print("Starting continuous analog reading...")
    print("Press Ctrl+C to stop")
    print("=" * 40)
    
    try:
        while True:
            raw_value, voltage, normalized = read_analog_value()
            print("-" * 20)
            time.sleep({{ interval }})
            
    except KeyboardInterrupt:
        print("\nStopping analog read...")
        print("Analog read stopped.")

# Perform the analog read
continuous = "{{ continuous }}".lower() in ("true", "1", "yes", "on")
if continuous:
    continuous_read()
else:
    read_analog_value()

