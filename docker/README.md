# circremote Docker Setup

This directory contains Docker configuration for running circremote in a containerized environment.

## Quick Start

### Build the Image

```bash
# From the project root directory
docker build -f docker/Dockerfile -t circremote:latest .
```

### Run with Docker Compose

```bash
# Start the interactive circremote container
docker-compose -f docker/docker-compose.yml up circremote

# Run a specific command (recommended: use --remove-orphans to avoid warnings)
docker-compose -f docker/docker-compose.yml run --remove-orphans circremote-run /dev/ttyUSB0 BME280

# Run with custom config file
docker-compose -f docker/docker-compose.yml run --remove-orphans circremote-run -C /workspace/config.json /dev/ttyUSB0 BME280
```

**Note:** The `--remove-orphans` flag prevents "Found orphan containers" warnings that occur when Docker Compose detects containers from previous configurations.

## Services

### circremote (Interactive)
- Runs an interactive shell with circremote available
- Mounts your local configuration and workspace
- Good for development and testing

### circremote-run (Command Runner)
- Designed for running specific circremote commands
- Uses the `run` profile to avoid starting by default
- Perfect for CI/CD or scripted usage

## Volume Mounts

The Docker setup mounts several important directories:

- `~/.circremote` → `/home/circremote/.circremote` (read-only)
  - Your circremote configuration files
- `.` → `/workspace` (read-write)
  - Current directory for accessing local commands and files
- `/dev/bus/usb` → `/dev/bus/usb` (read-only)
  - USB device access for Linux systems
- `~/.cache/circup` → `/home/circremote/.cache/circup` (read-write)
  - circup cache for faster dependency installation

**Optional: CIRCUITPY Drive Mapping**
For circup to install libraries directly to your CircuitPython device, add the CIRCUITPY drive:

```yaml
volumes:
  # Linux
  - /media/$USER/CIRCUITPY:/media/circremote/CIRCUITPY:rw
  # macOS
  - /Volumes/CIRCUITPY:/media/circremote/CIRCUITPY:rw
  # Windows
  - C:/CIRCUITPY:/media/circremote/CIRCUITPY:rw
```

## Device Access

The container has access to common serial devices:
- `/dev/ttyUSB0`
- `/dev/ttyACM0`
- `/dev/ttyACM1`

## Dependencies

The Docker image includes:
- **circup**: CircuitPython dependency management tool
  - Automatically installed and available for circremote to use
  - Cache directory created with proper permissions for the circremote user
  - Cache is persisted via volume mount for faster installations
  - Can be configured via circremote's `-u` option or config file

## Usage Examples

### Basic Usage
```bash
# Show help
docker-compose -f docker/docker-compose.yml run --remove-orphans circremote-run --help

# List available commands
docker-compose -f docker/docker-compose.yml run --remove-orphans circremote-run -l

# Run a sensor command
docker-compose -f docker/docker-compose.yml run --remove-orphans circremote-run /dev/ttyUSB0 BME280

# Run with verbose output
docker-compose -f docker/docker-compose.yml run --remove-orphans circremote-run -v /dev/ttyUSB0 BME280
```

### With Custom Configuration
```bash
# Use a custom config file
docker-compose -f docker/docker-compose.yml run --remove-orphans circremote-run \
  -C /workspace/my_config.json /dev/ttyUSB0 BME280

# Skip circup installation
docker-compose -f docker/docker-compose.yml run --remove-orphans circremote-run \
  -c /dev/ttyUSB0 BME280

# Use custom circup path (circup is installed in the container)
docker-compose -f docker/docker-compose.yml run --remove-orphans circremote-run \
  -u /usr/local/bin/circup /dev/ttyUSB0 BME280

# Test circup installation
docker run --rm circremote:latest circup --version

### With CIRCUITPY Drive Mapping
```bash
# First, add CIRCUITPY volume to docker-compose.yml
# Then run with library installation
docker-compose -f docker/docker-compose.yml run --remove-orphans circremote-run \
  /dev/ttyUSB0 BME280

# Check installed libraries on device
docker-compose -f docker/docker-compose.yml run --remove-orphans circremote-run \
  -u /usr/local/bin/circup /dev/ttyUSB0 --list
```

## Troubleshooting

### circup Permission Errors
If you encounter `PermissionError: [Errno 13] Permission denied: '/home/circremote/.cache/circup/log'`:

```bash
# Rebuild the Docker image to ensure proper cache directory permissions
docker build -f docker/Dockerfile -t circremote:latest .

# Test circup after rebuilding
docker run --rm circremote:latest circup --version
```

### circup Not Found
If circremote can't find circup:

```bash
# Check circup installation (bypass entrypoint)
docker run --rm --entrypoint="" circremote:latest /usr/local/bin/circup --version

# Test cache permissions
docker run --rm --entrypoint="" circremote:latest ls -la /home/circremote/.cache/circup/

# Use make targets for testing
make test-circup
make test-cache-permissions
```

### WebSocket Connections
```bash
# Connect to device over WiFi
docker-compose -f docker/docker-compose.yml run circremote-run \
  192.168.1.100:8080 BME280

# With password
docker-compose -f docker/docker-compose.yml run circremote-run \
  -p mypassword 192.168.1.100:8080 BME280
```

### Local Commands
```bash
# Run a local Python file
docker-compose -f docker/docker-compose.yml run circremote-run \
  /dev/ttyUSB0 /workspace/my_sensor.py

# Run a local command directory
docker-compose -f docker/docker-compose.yml run circremote-run \
  /dev/ttyUSB0 /workspace/custom_sensors/BME280
```

## Development

### Interactive Development
```bash
# Start interactive shell
docker-compose -f docker/docker-compose.yml up circremote

# In another terminal, execute commands
docker exec -it circremote circremote /dev/ttyUSB0 BME280
```

### Building for Different Platforms
```bash
# Build for ARM64 (Apple Silicon, Raspberry Pi)
docker buildx build --platform linux/arm64 -f docker/Dockerfile -t circremote:arm64 .

# Build for AMD64 (Intel/AMD)
docker buildx build --platform linux/amd64 -f docker/Dockerfile -t circremote:amd64 .
```

## Troubleshooting

### Permission Issues
If you encounter permission issues with device access:

```bash
# Add your user to the dialout group (Linux)
sudo usermod -a -G dialout $USER

# Or run with privileged mode (not recommended for production)
docker-compose -f docker/docker-compose.yml run --privileged circremote-run /dev/ttyUSB0 BME280
```

### Device Not Found
If your device uses a different port:

```bash
# List available devices
ls -la /dev/tty*

# Update docker-compose.yml with the correct device path
```

### Configuration Issues
If your config file isn't being read:

```bash
# Check if the config file exists
ls -la ~/.circremote/

# Mount the config file explicitly
docker-compose -f docker/docker-compose.yml run \
  -v $(pwd)/my_config.json:/home/circremote/.circremote/config.json:ro \
  circremote-run /dev/ttyUSB0 BME280
```

## Security Notes

- The container runs as a non-root user (`circremote`)
- Configuration files are mounted read-only
- USB device access is limited to specific devices
- Network access is restricted to host network mode

## License

This Docker setup is licensed under the MIT License, same as the main circremote project. 