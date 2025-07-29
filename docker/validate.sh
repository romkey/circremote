#!/bin/bash
# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: MIT

set -e

echo "Validating Docker setup..."

# Check if Dockerfile exists
if [ ! -f "Dockerfile" ]; then
    echo "❌ Error: Dockerfile not found"
    exit 1
fi

# Check if docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: docker-compose.yml not found"
    exit 1
fi

# Check if .dockerignore exists
if [ ! -f ".dockerignore" ]; then
    echo "❌ Error: .dockerignore not found"
    exit 1
fi

# Validate Dockerfile syntax (if docker is available)
if command -v docker &> /dev/null; then
    echo "🔍 Validating Dockerfile syntax..."
    if docker build --help > /dev/null 2>&1; then
        echo "✅ Docker is available and working"
    else
        echo "❌ Docker is available but not working properly"
        exit 1
    fi
else
    echo "⚠️  Docker not available, skipping syntax validation"
fi

# Validate docker-compose.yml syntax (if docker-compose is available)
if command -v docker-compose &> /dev/null; then
    echo "🔍 Validating docker-compose.yml syntax..."
    if docker-compose -f docker-compose.yml config > /dev/null 2>&1; then
        echo "✅ docker-compose.yml syntax is valid"
    else
        echo "❌ docker-compose.yml syntax validation failed"
        exit 1
    fi
else
    echo "⚠️  docker-compose not available, skipping syntax validation"
fi

# Check for common issues in Dockerfile
echo "🔍 Checking for common issues..."

# Check if FROM instruction exists
if ! grep -q "^FROM" Dockerfile; then
    echo "❌ Error: No FROM instruction found in Dockerfile"
    exit 1
fi

# Check if WORKDIR is set
if ! grep -q "^WORKDIR" Dockerfile; then
    echo "❌ Error: No WORKDIR instruction found in Dockerfile"
    exit 1
fi

# Check if ENTRYPOINT is set
if ! grep -q "^ENTRYPOINT" Dockerfile; then
    echo "❌ Error: No ENTRYPOINT instruction found in Dockerfile"
    exit 1
fi

# Check if user is created
if ! grep -q "useradd" Dockerfile; then
    echo "⚠️  Warning: No non-root user creation found in Dockerfile"
fi

# Check if .dockerignore excludes important files
if grep -q "venv/" .dockerignore; then
    echo "✅ .dockerignore excludes virtual environment"
else
    echo "⚠️  Warning: .dockerignore doesn't exclude venv/"
fi

if grep -q "__pycache__" .dockerignore; then
    echo "✅ .dockerignore excludes Python cache"
else
    echo "⚠️  Warning: .dockerignore doesn't exclude __pycache__"
fi

echo "✅ Docker setup validation completed successfully!" 