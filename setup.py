#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: MIT

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cpctrl",
    version="1.0.0",
    author="John Romkey",
    description="A command-line tool for uploading and running Python code on CircuitPython devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
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
    entry_points={
        "console_scripts": [
            "cpctrl=cpctrl.cli:main",
        ],
    },
) 