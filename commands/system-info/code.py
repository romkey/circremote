# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

import os
import sys
import gc
import board
import microcontroller

cp_info = os.uname().version.split(' on ')
print(f'''CircuitPython Version: {cp_info[0]}
CircuitPython Date: {cp_info[1]}
''')

print(os.uname().machine)
print(board.board_id)

try:
# SPDX-FileCopyrightText: 2020 anecdata
#
# SPDX-License-Identifier: MIT

# from https://gist.github.com/anecdata/1c345cb2d137776d76b97a5d5678dc97
    for pin in dir(microcontroller.pin):
        if isinstance(getattr(microcontroller.pin, pin), microcontroller.Pin):
            print("".join(("microcontroller.pin.", pin, "\t")), end=" ")
            for alias in dir(board):
                if getattr(board, alias) is getattr(microcontroller.pin, pin):
                    print("".join(("", "board.", alias)), end=" ")
        print()

except Exception as e:
    print(f"Could not get pin info (Error: {e})")

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
