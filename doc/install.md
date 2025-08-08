# Install `circremote`

### From PyPI

```bash
pip install circremote
```

### From Github
```
pip install git+https://github.com/romkey/circremote
```

### From Source

```bash
git clone https://github.com/romkey/circremote
cd circremote-python
pip install -e .
```

### Using Docker

```bash
# Build the Docker image (includes circup for dependency management)
docker build -f docker/Dockerfile -t circremote:latest .

# Run circremote in a container with a serial port
CIRCREMOTE_SERIAL=/dev/ttyUSB0 docker-compose -f docker/docker-compose.yml run circremote-serial /dev/ttyUSB0 BME280

# Run circremote in a container with a networked device
docker-compose -f docker/docker-compose.yml run circremote 192.168.1.100 -p PASSWORD  BME280

# Test circup installation
docker run --rm circremote:latest circup --version

# For more Docker options, see [docker/README.md](docker/README.md)
```
