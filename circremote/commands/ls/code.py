# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import os
import time

def is_directory(path):
    """Check if path is a directory using os.stat()"""
    try:
        stat = os.stat(path)
        # In CircuitPython, directories have stat[0] == 0x4000
        return (stat[0] & 0x4000) != 0
    except OSError:
        return False

def basename(path):
    """Get the basename of a path (CircuitPython compatible)"""
    if path == "/":
        return "/"
    # Split by '/' and get the last part
    parts = path.split("/")
    # Remove empty parts and get the last non-empty part
    for part in reversed(parts):
        if part:
            return part
    return "/"

def format_size(size):
    """Format file size in human readable format"""
    if size < 1024:
        return f"{size}B"
    elif size < 1024 * 1024:
        return f"{size // 1024}KB"
    else:
        return f"{size // (1024 * 1024)}MB"

def format_date(timestamp):
    """Format modification date in human friendly format"""
    try:
        # Convert timestamp to local time
        local_time = time.localtime(timestamp)
        # Format as YYYY-MM-DD HH:MM:SS
        return f"{local_time[0]:04d}-{local_time[1]:02d}-{local_time[2]:02d} {local_time[3]:02d}:{local_time[4]:02d}:{local_time[5]:02d}"
    except:
        # Fallback to timestamp if time formatting fails
        return str(timestamp)

def list_file_info(path, indent=""):
    """List information about a single file"""
    try:
        stat = os.stat(path)
        size = stat[6]  # st_size
        mtime = stat[8]  # st_mtime
        filename = basename(path)
        
        if is_directory(path):
            # Directory - show name only with fixed width columns
            size_str = "     "  # 5 spaces for directory
            date_str = "                    "  # 20 spaces for directory
            print(f"{size_str} {date_str} {indent}{filename}/")
        else:
            # File - show size, date, then name with indentation
            size_str = format_size(size)
            date_str = format_date(mtime)
            # Fixed width columns: size (8 chars) + space + date (19 chars) + space
            print(f"{size_str:>8} {date_str} {indent}{filename}")
        
    except OSError as e:
        print(f"{'':>8} {'':>19} {indent}ERROR: {path} - {e}")

def list_directory_recursive(path, indent=""):
    """Recursively list directory contents"""
    try:
        # List the directory itself
        list_file_info(path, indent)
        
        # List contents
        try:
            items = os.listdir(path)
            items.sort()  # Sort alphabetically
            
            for item in items:
                item_path = f"{path}/{item}" if path != "/" else f"/{item}"
                
                if is_directory(item_path):
                    # Recursively list subdirectories with increased indentation
                    list_directory_recursive(item_path, indent + "  ")
                else:
                    # List files
                    list_file_info(item_path, indent + "  ")
                    
        except OSError as e:
            print(f"{'':>8} {'':>19} {indent}ERROR: Cannot read directory {path} - {e}")
            
    except OSError as e:
        print(f"{'':>8} {'':>19} {indent}ERROR: {path} - {e}")

target = "{{ filename }}"

print(f"Listing: {target}")
print("-" * 50)

try:
    if is_directory(target):
        # Directory - do recursive listing
        list_directory_recursive(target)
    else:
        # File - list just that file
        list_file_info(target)
        
except OSError as e:
    print(f"ERROR: {e}")
