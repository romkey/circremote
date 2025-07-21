#!/usr/bin/env python3
"""
Test runner script with graceful interruption handling.
"""

import sys
import subprocess
import signal
import os


def signal_handler(signum, frame):
    """Handle interruption signals gracefully."""
    print("\n\nInterrupted by user. Exiting gracefully...")
    sys.exit(0)


def main():
    """Run tests with graceful interruption handling."""
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Build pytest command with quiet options
    cmd = [
        sys.executable, "-m", "pytest",
        "--quiet",
        "--tb=short",
        "--disable-warnings",
        "--maxfail=10",
        "--durations=10"
    ]
    
    # Add any additional arguments passed to the script
    cmd.extend(sys.argv[1:])
    
    try:
        # Run pytest as a subprocess
        result = subprocess.run(cmd, check=False)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"Error running tests: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 