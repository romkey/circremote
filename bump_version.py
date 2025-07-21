#!/usr/bin/env python3
import re
import sys
from pathlib import Path

VERSION_FILE = Path("circremote/version.py")

def get_current_version():
    content = VERSION_FILE.read_text()
    match = re.search(r'VERSION\s*=\s*["\']([^"\']+)["\']', content)
    if not match:
        raise RuntimeError("Cannot find VERSION in circremote/version.py")
    return match.group(1)

def bump_version(version, part):
    major, minor, patch = map(int, version.split("."))
    if part == "major":
        return f"{major+1}.0.0"
    elif part == "minor":
        return f"{major}.{minor+1}.0"
    elif part == "patch":
        return f"{major}.{minor}.{patch+1}"
    else:
        raise ValueError("part must be 'major', 'minor', or 'patch'")

def set_version(new_version):
    content = VERSION_FILE.read_text()
    new_content = re.sub(
        r'VERSION\s*=\s*["\']([^"\']+)["\']',
        f'VERSION = "{new_version}"',
        content
    )
    VERSION_FILE.write_text(new_content)

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("major", "minor", "patch"):
        print("Usage: bump_version.py [major|minor|patch]")
        sys.exit(1)
    part = sys.argv[1]
    current = get_current_version()
    new = bump_version(current, part)
    set_version(new)
    print(f"Bumped version: {current} -> {new}")

if __name__ == "__main__":
    main() 