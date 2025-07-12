# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import neopixel

pixels = neopixel.NeoPixel({{ neopixel_pin }}, {{ neopixel_count }}, brightness={{ brightness }}, auto_write=False)

while True:
    pixels.fill((255, 0, 0))
    pixels.show()
    time.sleep(0.5)

    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(0.5)
