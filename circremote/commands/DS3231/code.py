# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio
import adafruit_ds3231

# Initialize I2C with fallback
try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()

# Initialize DS3231
try:
    rtc = adafruit_ds3231.DS3231(i2c)
except Exception as e:
    print(f"Error initializing DS3231: {e}")
    import sys
    sys.exit(1)

print("DS3231 High-Accuracy Real-Time Clock")
print("=" * 40)

# Display RTC information
print(f"Temperature: {rtc.temperature:.1f}°C")
print(f"Lost Power: {rtc.lost_power}")
print()

# Function to format time
def format_time(t):
    return f"{t.tm_year:04d}-{t.tm_mon:02d}-{t.tm_mday:02d} {t.tm_hour:02d}:{t.tm_min:02d}:{t.tm_sec:02d}"

# Function to get day name
def get_day_name(weekday):
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    return days[weekday]

while True:
    # Get current time
    current_time = rtc.datetime
    
    print(f"Current Time: {format_time(current_time)}")
    print(f"Day of Week: {current_time.tm_wday} ({get_day_name(current_time.tm_wday)})")
    print(f"Day of Year: {current_time.tm_yday}")
    print(f"Temperature: {rtc.temperature:.1f}°C")
    print(f"Power Status: {'Lost' if rtc.lost_power else 'OK'}")
    print("-" * 30)
    
    time.sleep(10)
