# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import os
import re
import storage

def is_unwanted_file(filename):
    """Check if a file matches patterns of unwanted files."""
    
    # macOS patterns
    if filename.startswith('._') and len(filename) > 2:
        return True
    if filename == '.DS_Store':
        return True
    if filename == '.Spotlight-V100':
        return True
    if filename == '.fseventsd':
        return True
    if filename == '.Trashes':
        return True
    if re.match(r'\.Trash-\d+', filename):
        return True
    
    # Windows patterns
    if filename == 'System Volume Information':
        return True
    if filename == '$RECYCLE.BIN':
        return True
    if filename == 'Thumbs.db':
        return True
    if filename == 'Desktop.ini':
        return True
    
    # Linux patterns
    if filename == '.directory':
        return True
    if re.match(r'\.Trash-\d+', filename):
        return True
    if filename == '.recently-used.xbel':
        return True
    if filename == '.recently-used':
        return True
    if re.match(r'\.goutputstream-[A-Za-z0-9]+\.tmp', filename):
        return True
    
    # Emacs patterns
    if filename.startswith('.#') and len(filename) > 2:
        return True
    if filename.endswith('~'):
        return True
    if filename.startswith('#') and filename.endswith('#'):
        return True
    if filename.endswith('.swp'):
        return True
    if filename.endswith('.swp~'):
        return True
    if filename.endswith('.lock'):
        return True
    
    # Vi patterns
    if filename.endswith('.swp'):
        return True
    if filename.endswith('.un~'):
        return True
    
    return False

def scan_for_unwanted_files(root_path):
    """Scan the filesystem for unwanted files using CircuitPython's filesystem API."""
    unwanted_files = []
    
    def scan_directory(path):
        """Recursively scan a directory for unwanted files."""
        try:
            # List all items in the directory
            items = os.listdir(path)
            
            for item in items:
                item_path = path + "/" + item if path != "/" else "/" + item
                
                # Check if this item is unwanted
                if is_unwanted_file(item):
                    unwanted_files.append(item_path)
                    continue  # Don't recurse into unwanted directories
                
                # Check if it's a directory and recurse
                try:
                    # Try to list the directory to see if it's a directory
                    os.listdir(item_path)
                    # If we get here, it's a directory, so recurse
                    scan_directory(item_path)
                except OSError:
                    # Not a directory or can't access, skip
                    pass
                    
        except OSError as e:
            print(f"Error scanning directory {path}: {e}")
    
    try:
        scan_directory(root_path)
    except OSError as e:
        print(f"Error scanning filesystem: {e}")
        return []
    
    return unwanted_files

def check_and_make_filesystem_writable():
    """Check if filesystem is mounted by USB host and attempt to make it writable."""
    try:
        storage.remount("/", readonly=False)
        print("Filesystem not mounted by USB host (writable)")
        return True
    except OSError:
        print("Filesystem is mounted by USB host (read-only)")
        return False

def main():
    """Main function for the clean command."""
    delete = {{delete}}
    
    print("Scanning for unwanted files...")
    print("(macOS, Windows, Linux, Emacs, Vi temporary files)")
    print()
    
    # Start from root directory
    root_path = "/"
    unwanted_files = scan_for_unwanted_files(root_path)
    
    if not unwanted_files:
        print("No unwanted files found!")
        return
    
    print(f"Found {len(unwanted_files)} unwanted file(s):")
    print()
    
    for file_path in sorted(unwanted_files):
        print(f"  {file_path}")
    
    print()
    
    if delete:
        # Check if filesystem is writable and attempt to make it writable
        if not check_and_make_filesystem_writable():
            print("❌ Error: Cannot delete files - filesystem is read-only!")
            print()
            print("The CircuitPython filesystem is currently mounted on your computer.")
            print("To delete files, you must:")
            print("  1. Unmount/eject the CIRCUITPY drive from your computer")
            print("  2. Run the clean command again")
            print()
            print("On macOS/Linux: unmount the CIRCUITPY drive")
            print("On Windows: safely eject the CIRCUITPY drive")
            print()
            print("After unmounting, the device will be writable again.")
            return
        
        print("Deleting unwanted files...")
        deleted_count = 0
        failed_count = 0
        
        for file_path in unwanted_files:
            try:
                # Try to remove as a file first
                try:
                    os.remove(file_path)
                    print(f"  Deleted file: {file_path}")
                except OSError:
                    # If that fails, try to remove as a directory
                    try:
                        os.rmdir(file_path)
                        print(f"  Deleted directory: {file_path}")
                    except OSError as dir_error:
                        print(f"  Failed to delete {file_path}: {dir_error}")
                        failed_count += 1
                        continue
                deleted_count += 1
            except OSError as e:
                print(f"  Failed to delete {file_path}: {e}")
                failed_count += 1
        
        print()
        print(f"Deleted {deleted_count} file(s)")
        if failed_count > 0:
            print(f"Failed to delete {failed_count} file(s)")
    else:
        print("To delete these files, run the command again with delete=1")
        print("Example: circremote /dev/ttyUSB0 clean delete=1")

if __name__ == "__main__":
    main() 
