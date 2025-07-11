# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

import os
import sys
import gc

cp_version = sys.implementation.version
cp_version_str = '.'.join(str(v) for v in cp_version)
print(f'''
System Information:
CircuitPython Version: {cp_version_str}
''')

try:
    import board

    print(f"Board {board.board_id}")

    pins = []
    for item in dir(board):
        if not item.startswith('__') and not item.startswith('_') and item.isupper():
            pins.append(item)
    
    if pins:
        print(f"Available Pins: {', '.join(pins)}")

except (ImportError, AttributeError) as e:
    print("Could not get pins")

try:
    fs_stat = os.statvfs('/')
    flash_size = fs_stat[0] * fs_stat[2]  # Block size * Total blocks
    flash_free = fs_stat[0] * fs_stat[3]  # Block size * Free blocks
    print(f'''
Flash Size: {flash_size} bytes
Flash Free: {flash_free} bytes
''')
except (OSError, AttributeError) as e:
    flash_out = f"Flash info unavailable (Error: {e})"

gc.collect()
try:
    mem_free = gc.mem_free()
    mem_alloc = gc.mem_alloc()
    mem_total = mem_free + mem_alloc
    print(f'''
Memory Total: {mem_total} bytes
Memory Free: {mem_free} bytes
''')
except Exception as e:
    print(f"Memory info unavailable (Error: {e})")

try:
    import wifi

    radio = wifi.radio
    if radio.connected:
        print(f'''
Connected to: {radio.ap_info.ssid}
RSSI: {radio.ap_info.rssi} dBm
Channel: {radio.ap_info.channel}
IP Address: {radio.ipv4_address}
''')
    else:
        print('Wifi not connected')

except (ImportError, AttributeError):
    print("No wifi")

