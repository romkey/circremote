# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

import os
import sys
import gc
import board
import microcontroller
import re

def natural_sort_key(s):
    """Sort key function for natural sorting of strings with numbers."""
    # Ensure we have a string to work with
    if not isinstance(s, str):
        s = str(s)
    
    # Simple implementation that works with CircuitPython's limited re support
    # Split on digits manually and pad numbers with zeros for proper string sorting
    result = ""
    current_num = ""
    
    for char in s:
        if char.isdigit():
            current_num += char
        else:
            if current_num:
                # Pad numbers with zeros to ensure proper sorting
                while len(current_num) < 10:
                    current_num = "0" + current_num
                result += current_num
                current_num = ""
            result += char.lower()
    
    # Handle any remaining number at the end
    if current_num:
        while len(current_num) < 10:
            current_num = "0" + current_num
        result += current_num
    
    return result

cp_info = os.uname().version.split(' on ')
print(f'''CircuitPython Version: {cp_info[0]}
CircuitPython Date: {cp_info[1]}
''')

print(os.uname().machine)
print(board.board_id)
print()


try:
# SPDX-FileCopyrightText: 2020 anecdata
#
# SPDX-License-Identifier: MIT

# from https://gist.github.com/anecdata/1c345cb2d137776d76b97a5d5678dc97
    # Get all pin names and sort them naturally
    pin_names = []
    for pin in dir(microcontroller.pin):
        if isinstance(getattr(microcontroller.pin, pin), microcontroller.Pin):
            if isinstance(pin, str):
                pin_names.append(pin)
    
    # Sort pin names using natural sorting
    pin_names.sort(key=natural_sort_key)
    
    for pin in pin_names:
        print("".join(("microcontroller.pin.", pin, "\t")), end=" ")
        for alias in dir(board):
            if getattr(board, alias) is getattr(microcontroller.pin, pin):
                print("".join(("", "board.", alias)), end=" ")
        print()

    print()

except Exception as e:
    print(f"Could not get pin info (Error: {e})")
    import traceback
    traceback.print_exc()

# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0
try:
    fs_stat = os.statvfs('/')
    flash_size = fs_stat[0] * fs_stat[2]  # Block size * Total blocks
    flash_free = fs_stat[0] * fs_stat[3]  # Block size * Free blocks
    print(f'''Flash Size: {flash_size} bytes
Flash Free: {flash_free} bytes
''')
except (OSError, AttributeError) as e:
    flash_out = f"Flash info unavailable (Error: {e})"

gc.collect()
try:
    mem_free = gc.mem_free()
    mem_alloc = gc.mem_alloc()
    mem_total = mem_free + mem_alloc
    print(f'''Memory Total: {mem_total} bytes
Memory Free: {mem_free} bytes
''')
except Exception as e:
    print(f"Memory info unavailable (Error: {e})")

try:
    import wifi

    radio = wifi.radio
    if radio.connected:
        bssid = ":".join("%02x" % b for b in radio.ap_info.bssid)
        mac_address =  ":".join("%02x" % b for b in wifi.radio.mac_address)

        print(f'''SSID: {radio.ap_info.ssid}
BSSID: {bssid}
RSSI: {radio.ap_info.rssi} dBm
Channel: {radio.ap_info.channel}
IP Address: {radio.ipv4_address}
MAC Address: {mac_address}
''')
    else:
        print('Wifi not connected')

except (ImportError, AttributeError):
    print("No wifi")
