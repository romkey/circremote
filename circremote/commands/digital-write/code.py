# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import digitalio

# Pin configuration
pin = {{ pin }}
level = "{{ level }}"
mode = "{{ mode }}"

print(f"Digital Write")
print(f"Pin: {pin}")
print(f"Level: {level}")

# Initialize digital output
digital_pin = digitalio.DigitalInOut(pin)
digital_pin.direction = digitalio.Direction.OUTPUT

def write_digital_value(value):
    """Write digital value to the pin."""
    try:
        # Convert level to boolean
        if isinstance(value, str):
            if value.upper() in ['HIGH', '1', 'TRUE', 'ON']:
                bool_value = True
            elif value.upper() in ['LOW', '0', 'FALSE', 'OFF']:
                bool_value = False
            else:
                print(f"Error: Invalid level '{value}'. Use HIGH/LOW, 1/0, TRUE/FALSE, or ON/OFF")
                return False
        elif isinstance(value, (int, float)):
            bool_value = bool(value)
        else:
            bool_value = bool(value)
        
        # Write the value
        digital_pin.value = bool_value
        
        print(f"Set pin {pin} to {bool_value}")
        print(f"Logic Level: {'HIGH' if bool_value else 'LOW'}")
        print(f"Voltage: {'3.3V (or 5V)' if bool_value else '0V'}")
        
        return True
        
    except Exception as e:
        print(f"Error writing to digital pin: {e}")
        return False

def toggle_output():
    """Toggle the output state."""
    print("Toggling output...")
    current_value = digital_pin.value
    new_value = not current_value
    write_digital_value(new_value)
    return new_value

def pulse_output(duration=1.0):
    """Send a pulse (HIGH for duration, then LOW)."""
    print(f"Sending {duration}s pulse...")
    write_digital_value(True)
    time.sleep(duration)
    write_digital_value(False)
    print("Pulse complete")

def blink_output(count=5, on_time=0.5, off_time=0.5):
    """Blink the output a specified number of times."""
    print(f"Blinking {count} times (on: {on_time}s, off: {off_time}s)...")
    
    for i in range(count):
        print(f"Blink {i+1}/{count}")
        write_digital_value(True)
        time.sleep(on_time)
        write_digital_value(False)
        if i < count - 1:  # Don't wait after the last blink
            time.sleep(off_time)
    
    print("Blinking complete")

# Perform the digital write
if mode == "toggle":
    toggle_output()
elif mode == "pulse":
    pulse_output({{ pulse_duration }})
elif mode == "blink":
    blink_output({{ blink_count }}, {{ blink_on_time }}, {{ blink_off_time }})
else:
    write_digital_value(level)

