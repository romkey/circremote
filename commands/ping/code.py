# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import wifi
import ipaddress

print(f"My address: {wifi.radio.ipv4_address}")

print("Ping {{ target }}")
dest = ipaddress.ip_address("{{ target }}")
while True:
    print("ping:", wifi.radio.ping(dest))
    time.sleep(1)
