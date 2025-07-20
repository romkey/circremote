# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

"""
CircuitPython tar implementation

Creates a tar archive and streams it to STDOUT.
Walks the filesystem starting from root and includes all files
with available metadata.
"""

import os
import sys

# Tar header constants
BLOCK_SIZE = 512
HEADER_SIZE = 512

# Tar header field sizes
NAME_SIZE = 100
MODE_SIZE = 8
UID_SIZE = 8
GID_SIZE = 8
SIZE_SIZE = 12
MTIME_SIZE = 12
CHKSUM_SIZE = 8
TYPE_SIZE = 1
LINKNAME_SIZE = 100
MAGIC_SIZE = 6
VERSION_SIZE = 2
UNAME_SIZE = 32
GNAME_SIZE = 32
DEVMAJOR_SIZE = 8
DEVMINOR_SIZE = 8
PREFIX_SIZE = 155

# Tar header field offsets
NAME_OFFSET = 0
MODE_OFFSET = NAME_OFFSET + NAME_SIZE
UID_OFFSET = MODE_OFFSET + MODE_SIZE
GID_OFFSET = UID_OFFSET + UID_SIZE
SIZE_OFFSET = GID_OFFSET + GID_SIZE
MTIME_OFFSET = SIZE_OFFSET + SIZE_SIZE
CHKSUM_OFFSET = MTIME_OFFSET + MTIME_SIZE
TYPE_OFFSET = CHKSUM_OFFSET + CHKSUM_SIZE
LINKNAME_OFFSET = TYPE_OFFSET + TYPE_SIZE
MAGIC_OFFSET = LINKNAME_OFFSET + LINKNAME_SIZE
VERSION_OFFSET = MAGIC_OFFSET + MAGIC_SIZE
UNAME_OFFSET = VERSION_OFFSET + VERSION_SIZE
GNAME_OFFSET = UNAME_OFFSET + UNAME_SIZE
DEVMAJOR_OFFSET = GNAME_OFFSET + GNAME_SIZE
DEVMINOR_OFFSET = DEVMAJOR_OFFSET + DEVMAJOR_SIZE
PREFIX_OFFSET = DEVMINOR_OFFSET + DEVMINOR_SIZE

# Tar constants
TAR_MAGIC = b'ustar'
TAR_VERSION = b'00'
REGULAR_FILE = b'0'
DIRECTORY = b'5'

def octal_string(value, size):
    """Convert a number to an octal string of specified size."""
    if value is None:
        value = 0
    octal_str = f"{value:o}"
    # Pad with zeros to size-1, then add space
    while len(octal_str) < size - 1:
        octal_str = '0' + octal_str
    return (octal_str + ' ').encode('ascii')

def string_field(value, size):
    """Convert a string to a field of specified size."""
    if value is None:
        value = ""
    encoded = value.encode('ascii')
    # Pad with null bytes to size
    while len(encoded) < size:
        encoded += b'\0'
    return encoded

def calculate_checksum(header):
    """Calculate the checksum for a tar header."""
    # Replace checksum field with spaces
    header_with_spaces = header[:CHKSUM_OFFSET] + b' ' * CHKSUM_SIZE + header[CHKSUM_OFFSET + CHKSUM_SIZE:]
    return sum(header_with_spaces)

def get_file_size(file_path):
    """Get file size by reading the file."""
    try:
        size = 0
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(BLOCK_SIZE)
                if not chunk:
                    break
                size += len(chunk)
        return size
    except OSError:
        return 0

def is_directory(path):
    """Check if path is a directory by trying to list it."""
    try:
        os.listdir(path)
        return True
    except OSError:
        return False

def create_tar_header(path, is_dir=False, file_size=0):
    """Create a tar header for a file."""
    header = bytearray(HEADER_SIZE)
    
    # File name (truncate if too long)
    name = path.encode('ascii')
    if len(name) > NAME_SIZE:
        name = name[:NAME_SIZE]
    header[NAME_OFFSET:NAME_OFFSET + len(name)] = name
    
    # File mode (default permissions)
    if is_dir:
        mode = 0o755  # rwxr-xr-x for directories
    else:
        mode = 0o644  # rw-r--r-- for files
    header[MODE_OFFSET:MODE_OFFSET + MODE_SIZE] = octal_string(mode, MODE_SIZE)
    
    # User ID (default to 0)
    header[UID_OFFSET:UID_OFFSET + UID_SIZE] = octal_string(0, UID_SIZE)
    
    # Group ID (default to 0)
    header[GID_OFFSET:GID_OFFSET + GID_SIZE] = octal_string(0, GID_SIZE)
    
    # File size (only for regular files)
    if not is_dir:
        header[SIZE_OFFSET:SIZE_OFFSET + SIZE_SIZE] = octal_string(file_size, SIZE_SIZE)
    else:
        header[SIZE_OFFSET:SIZE_OFFSET + SIZE_SIZE] = octal_string(0, SIZE_SIZE)
    
    # Modification time (use current time)
    current_time = 0  # Could use time.time() if available
    header[MTIME_OFFSET:MTIME_OFFSET + MTIME_SIZE] = octal_string(current_time, MTIME_SIZE)
    
    # File type
    if is_dir:
        file_type = DIRECTORY
    else:
        file_type = REGULAR_FILE
    header[TYPE_OFFSET:TYPE_OFFSET + TYPE_SIZE] = file_type
    
    # Magic and version
    header[MAGIC_OFFSET:MAGIC_OFFSET + MAGIC_SIZE] = TAR_MAGIC
    header[VERSION_OFFSET:VERSION_OFFSET + VERSION_SIZE] = TAR_VERSION
    
    # User name (default to "root")
    header[UNAME_OFFSET:UNAME_OFFSET + UNAME_SIZE] = string_field("root", UNAME_SIZE)
    
    # Group name (default to "root")
    header[GNAME_OFFSET:GNAME_OFFSET + GNAME_SIZE] = string_field("root", GNAME_SIZE)
    
    # Calculate and set checksum
    checksum = calculate_checksum(header)
    header[CHKSUM_OFFSET:CHKSUM_OFFSET + CHKSUM_SIZE] = octal_string(checksum, CHKSUM_SIZE)
    
    return bytes(header)

def write_file_content(file_path):
    """Write file content to STDOUT in blocks."""
    try:
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(BLOCK_SIZE)
                if not chunk:
                    break
                sys.stdout.write(chunk)
            
            # Pad to block boundary
            remainder = len(chunk) % BLOCK_SIZE
            if remainder > 0:
                padding = BLOCK_SIZE - remainder
                sys.stdout.write(b'\0' * padding)
    except OSError as e:
        # Skip files we can't read
        pass

def walk_filesystem(start_path="/"):
    """Recursively walk the filesystem and yield file and directory paths."""
    stack = [start_path]
    while stack:
        path = stack.pop()
        # Always yield the directory or file itself
        yield path
        if is_directory(path):
            try:
                for entry in os.listdir(path):
                    # Skip . and .. if present
                    if entry in (".", ".."):
                        continue
                    full_path = path.rstrip("/") + "/" + entry
                    stack.append(full_path)
            except OSError:
                pass

def create_tar_archive():
    """Create and stream a tar archive to STDOUT."""
    for file_path in walk_filesystem():
        try:
            # Check if it's a directory
            is_dir = is_directory(file_path)
            
            # Get file size for regular files
            file_size = 0
            if not is_dir:
                file_size = get_file_size(file_path)
            
            # Create and write header
            header = create_tar_header(file_path, is_dir, file_size)
            sys.stdout.write(header)
            
            # Write file content for regular files
            if not is_dir:
                write_file_content(file_path)
        
        except OSError as e:
            # Skip files we can't process
            continue
    
    # Write two empty blocks to mark end of archive
    sys.stdout.write(b'\0' * BLOCK_SIZE * 2)

if __name__ == "__main__":
    create_tar_archive() 




