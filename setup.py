#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: MIT

from setuptools import setup, find_packages
import re

def read_version():
    with open("circremote/version.py", "r") as f:
        content = f.read()
    match = re.search(r'VERSION\s*=\s*["\']([^"\']+)["\']', content)
    if not match:
        raise RuntimeError("Cannot find VERSION in circremote/version.py")
    return match.group(1)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="circremote",
    version=read_version(),
    author="John Romkey",
    description="A command-line tool for uploading and running Python code on CircuitPython devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "circremote": ["commands/*/*", "commands/*/code.py", "commands/*/info.json", "commands/*/requirements.txt"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pyserial>=3.5",
        "websocket-client>=1.0.0",
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.10",
            "pytest-mock>=3.0",
            "tox>=3.0",
            "flake8>=3.8",
            "black>=21.0",
            "isort>=5.0",
            "sphinx>=3.0",
            "sphinx-rtd-theme>=0.5",
        ],
    },
    entry_points={
        "console_scripts": [
            "circremote=circremote.cli:main",
        ],
    },
) 