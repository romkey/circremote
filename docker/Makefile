# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: MIT

# Variables
IMAGE_NAME = circremote
TAG = latest
DOCKERFILE = Dockerfile
COMPOSE_FILE = docker-compose.yml
CONTEXT = ..

# Default target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  build        - Build the circremote Docker image"
	@echo "  run          - Run circremote interactively"
	@echo "  exec         - Execute a specific circremote command"
	@echo "  clean        - Remove circremote Docker images"
	@echo "  test         - Test the Docker image"
	@echo "  test-circup  - Test circup installation"
	@echo "  test-circuitpy - Test CIRCUITPY drive access"
	@echo "  test-cache-permissions - Test circup cache directory permissions"
	@echo "  push         - Push the image to registry (requires login)"
	@echo "  multiarch    - Build multi-architecture image"

# Build the Docker image
.PHONY: build
build:
	docker build -f $(DOCKERFILE) -t $(IMAGE_NAME):$(TAG) $(CONTEXT)

# Run circremote interactively
.PHONY: run
run:
	docker-compose -f $(COMPOSE_FILE) up circremote

# Execute a specific command (usage: make exec CMD="/dev/ttyUSB0 BME280")
.PHONY: exec
exec:
	@if [ -z "$(CMD)" ]; then \
		echo "Usage: make exec CMD='<circremote command>'"; \
		echo "Example: make exec CMD='/dev/ttyUSB0 BME280'"; \
		exit 1; \
	fi
	docker-compose -f $(COMPOSE_FILE) run --remove-orphans --rm circremote-run $(CMD)

# Test the Docker image
.PHONY: test
test:
	docker run --rm $(IMAGE_NAME):$(TAG) --version
	docker run --rm $(IMAGE_NAME):$(TAG) --help

# Clean up Docker images
.PHONY: clean
clean:
	docker rmi $(IMAGE_NAME):$(TAG) 2>/dev/null || true
	docker rmi $(IMAGE_NAME):test 2>/dev/null || true

# Build multi-architecture image
.PHONY: multiarch
multiarch:
	docker buildx build --platform linux/amd64,linux/arm64 \
		-f $(DOCKERFILE) \
		-t $(IMAGE_NAME):$(TAG) \
		$(CONTEXT)

# Push to registry (requires docker login)
.PHONY: push
push:
	docker push $(IMAGE_NAME):$(TAG)

# Development helpers
.PHONY: dev-build
dev-build:
	docker build -f $(DOCKERFILE) -t $(IMAGE_NAME):dev $(CONTEXT)

.PHONY: dev-run
dev-run:
	docker run -it --rm \
		-v $(PWD):/workspace \
		-v ~/.circremote:/home/circremote/.circremote:ro \
		--device=/dev/ttyUSB0 \
		--device=/dev/ttyACM0 \
		$(IMAGE_NAME):dev

# Quick commands
.PHONY: help-cmd
help-cmd:
	make exec CMD="--help"

.PHONY: list-cmd
list-cmd:
	make exec CMD="-l"

.PHONY: version
version:
	make exec CMD="--version"

.PHONY: test-circup
test-circup:
	docker run --rm --entrypoint="" circremote:latest /usr/local/bin/circup --version

.PHONY: test-circuitpy
test-circuitpy:
	@echo "Testing CIRCUITPY access..."
	@if [ -d "/media/$$USER/CIRCUITPY" ]; then \
		echo "Linux: CIRCUITPY found at /media/$$USER/CIRCUITPY"; \
	elif [ -d "/Volumes/CIRCUITPY" ]; then \
		echo "macOS: CIRCUITPY found at /Volumes/CIRCUITPY"; \
	else \
		echo "CIRCUITPY drive not found. Please check if your CircuitPython device is connected."; \
		echo "Linux: /media/$$USER/CIRCUITPY"; \
		echo "macOS: /Volumes/CIRCUITPY"; \
		echo "Windows: C:/CIRCUITPY"; \
	fi

.PHONY: test-cache-permissions
test-cache-permissions:
	@echo "Testing circup cache permissions..."
	docker run --rm --entrypoint="" circremote:latest ls -la /home/circremote/.cache/circup/ 