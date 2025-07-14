# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_apds9960.apds9960

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize APDS9960
try:
    apds = adafruit_apds9960.apds9960.APDS9960(i2c, address={{ address }})
except Exception as e:
    print(f"Error initializing APDS9960: {e}")
    import sys
    sys.exit(1)

print("APDS9960 Gesture & Color Sensor")
print("=" * 35)

# Enable color and gesture sensing
apds.enable_color = True
apds.enable_gesture = True
apds.enable_proximity = True

# Display sensor information
print(f"Color Integration Time: {apds.color_integration_time} ms")
print(f"Color Gain: {apds.color_gain}")
print(f"Proximity Gain: {apds.proximity_gain}")
print(f"Gesture Gain: {apds.gesture_gain}")
print(f"Gesture LED Drive: {apds.gesture_led_drive}")
print()

# Main reading loop
while True:
    # Read color data
    r, g, b, c = apds.color_data
    print(f"Color: R={r}, G={g}, B={b}, C={c}")
        
    # Read proximity data
    proximity = apds.proximity
    print(f"Proximity: {proximity}")
        
    # Read gesture data
    gesture = apds.gesture()
    if gesture == 0x01:
        print("Gesture: UP")
    elif gesture == 0x02:
        print("Gesture: DOWN")
    elif gesture == 0x03:
        print("Gesture: LEFT")
    elif gesture == 0x04:
        print("Gesture: RIGHT")
    else:
        print("Gesture: None")
            
    print("-" * 30)
        
    time.sleep(30)
