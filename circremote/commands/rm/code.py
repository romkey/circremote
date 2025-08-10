# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import os
import storage

def is_directory(path):
    """Check if path is a directory using os.stat()"""
    try:
        stat = os.stat(path)
        # In CircuitPython, directories have stat[0] == 0x4000
        return (stat[0] & 0x4000) != 0
    except OSError:
        return False

def check_and_make_filesystem_writable():
    """Check if filesystem is writable, try to make it writable if not"""
    try:
        storage.remount("/", readonly=False)
        return True
    except OSError:
        return False

def remove_file_or_directory(path):
    """Remove a file or directory recursively"""
    try:
        if is_directory(path):
            # Directory - remove recursively
            print(f"Removing directory: {path}")
            
            # First remove all contents
            try:
                items = os.listdir(path)
                for item in items:
                    item_path = f"{path}/{item}" if path != "/" else f"/{item}"
                    remove_file_or_directory(item_path)
                
                # Then remove the empty directory
                os.rmdir(path)
                print(f"✓ Removed directory: {path}")
                
            except OSError as e:
                print(f"✗ Failed to remove directory contents: {path} - {e}")
                return False
                
        else:
            # File - remove directly
            print(f"Removing file: {path}")
            os.remove(path)
            print(f"✓ Removed file: {path}")
            
        return True
        
    except OSError as e:
        print(f"✗ Failed to remove: {path} - {e}")
        return False

# Check if filesystem is mounted by USB host
if not check_and_make_filesystem_writable():
    print("ERROR: Filesystem is mounted by USB host (read-only)")
    print("Please eject the CIRCUITPY drive before running this command")
    exit(1)

target = "{{ filename }}"

print(f"Removing: {target}")
print("-" * 50)

if remove_file_or_directory(target):
    print("✓ Removal completed successfully")
else:
    print("✗ Some items could not be removed")
    exit(1)
