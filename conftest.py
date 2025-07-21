"""
Global pytest configuration for graceful interruption handling.
"""

import pytest
import signal
import sys


def pytest_configure(config):
    """Configure pytest for graceful interruption handling."""
    # Set up signal handlers for graceful interruption
    def signal_handler(signum, frame):
        print("\n\nInterrupted by user. Exiting gracefully...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)


def pytest_runtest_logreport(report):
    """Customize test reporting to reduce noise."""
    if report.when == 'call' and report.failed:
        # Only show detailed output for failed tests
        pass


 