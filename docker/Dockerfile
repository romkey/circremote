# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: MIT

FROM python:3.13.5-slim

# Set metadata
LABEL maintainer="John Romkey <58883+romkey@users.noreply.github.com>"
LABEL description="circremote - A command-line tool for uploading and running code on CircuitPython devices"
LABEL version="1.0.0"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the circremote source code
COPY . .

# Install circup for CircuitPython dependency management
RUN pip install circup

# Install circremote in development mode
RUN pip install -e .

# Create a non-root user for running circremote
RUN useradd -m -s /bin/bash circremote && \
    chown -R circremote:circremote /app

# Create circup cache directory with proper permissions
RUN mkdir -p /home/circremote/.cache/circup && \
    chown -R circremote:circremote /home/circremote/.cache

# Switch to non-root user
USER circremote

# Set the entrypoint to circremote
ENTRYPOINT ["circremote"]

# Default command (can be overridden)
CMD ["--help"] 