# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import board
from adafruit_onewire.bus import OneWireBus

ow_bus = OneWireBus({{ onewire_pin }})
devices = ow_bus.scan()
for d in devices:
    print(f"ROM={d.rom.hex()}\tFamily=0x{d.family_code:02x}")
