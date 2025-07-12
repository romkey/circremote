# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

try:
    with open("{{ filename }}", "r") as f:
        print("Current {{filename}} contents:")
        print("-" * 40)
        print(f.read())
        print("-" * 40)
except OSError:
    print("{{ filename }} not found")
