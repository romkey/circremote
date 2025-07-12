# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

try:
    with open("/settings.toml", "r") as f:
        settings_content = f.read()
        if settings_content.strip():
            print("Current settings.toml contents:")
            print("-" * 40)
            print(settings_content)
            print("-" * 40)
        else:
            print("settings.toml exists but is empty")
except OSError:
    print("settings.toml file not found")
