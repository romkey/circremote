# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
from adafruit_pcf8523.pcf8523 import PCF8523

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize PCF8523
try:
    rtc = PCF8523(i2c)
except Exception as e:
    print(f"Error initializing PCF8523: {e}")
    import sys
    sys.exit(1)

print("PCF8523 Real-Time Clock")
print("=" * 25)

# Display RTC information
print(f"Battery Low: {rtc.battery_low}")
print()

# Function to format time
def format_time(t):
    return f"{t.tm_year:04d}-{t.tm_mon:02d}-{t.tm_mday:02d} {t.tm_hour:02d}:{t.tm_min:02d}:{t.tm_sec:02d}"

while True:
    # Get current time
    current_time = rtc.datetime
    
    print(f"Current Time: {format_time(current_time)}")
    print(f"Day of Week: {current_time.tm_wday} ({['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][current_time.tm_wday]})")
    print(f"Day of Year: {current_time.tm_yday}")
    print(f"Battery Status: {'Low' if rtc.battery_low else 'OK'}")
    print("-" * 30)
    
    time.sleep(10)
