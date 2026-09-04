# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time

# adafruit_ble (and the underlying _bleio) is unavailable on boards without
# BLE support, so import it defensively and exit cleanly if it's missing.
try:
    from adafruit_ble import BLERadio
except ImportError:
    print("Error: adafruit_ble / _bleio not available.")
    print("This CircuitPython board does not appear to support Bluetooth LE.")
    raise SystemExit

# Configuration
max_scans = {{ max_scans }}
scan_interval = {{ scan_interval }}
test_mode = "{{ test_mode }}".lower() in ("true", "1", "yes", "on")

print("Bluetooth Scan")


def format_address(address):
    """Format a BLE address as a colon-separated hex string."""
    if address is None:
        return "Unknown"
    try:
        return ":".join("%02x" % b for b in address.address_bytes)
    except (AttributeError, TypeError):
        return str(address)


def format_rssi(rssi):
    """Format RSSI value with a signal strength interpretation."""
    if rssi is None:
        return "Unknown"

    if rssi >= -50:
        strength = "Excellent"
    elif rssi >= -60:
        strength = "Good"
    elif rssi >= -70:
        strength = "Fair"
    elif rssi >= -80:
        strength = "Weak"
    else:
        strength = "Very Weak"

    return f"{rssi} dBm ({strength})"


def get_name(advertisement):
    """Return the best available name from an advertisement."""
    name = getattr(advertisement, "complete_name", None)
    if not name:
        name = getattr(advertisement, "short_name", None)
    return name


def classify_device(name, connectable):
    """Best-effort device classification from the advertised name."""
    if name:
        lower = name.lower()
        keywords = (
            (("phone", "iphone", "android", "galaxy", "pixel"), "Phone"),
            (("laptop", "macbook", "thinkpad", "dell", "lenovo"), "Laptop"),
            (("airpods", "buds", "headphone", "earphone", "headset"), "Audio Device"),
            (("keyboard", "mouse", "trackpad", "touchpad"), "Input Device"),
            (("watch", "band", "fitbit", "wear"), "Wearable"),
            (("speaker", "sonos", "bose", "sound"), "Speaker"),
            (("tv", "television", "display", "monitor"), "TV/Display"),
            (("tablet", "ipad", "surface"), "Tablet"),
            (("sensor", "beacon", "tag", "tracker"), "IoT Device"),
        )
        for words, label in keywords:
            if any(word in lower for word in words):
                return label

    if connectable is False:
        return "Beacon/Broadcaster"
    return "Unknown"


def print_advertisement(address_str, advertisement):
    """Print information about a discovered advertisement."""
    rssi = getattr(advertisement, "rssi", None)
    connectable = getattr(advertisement, "connectable", None)
    name = get_name(advertisement)
    device_type = classify_device(name, connectable)

    print("\n--- Device Found ---")
    print(f"Address: {address_str}")
    print(f"RSSI: {format_rssi(rssi)}")
    print(f"Type: {device_type}")
    if name:
        print(f"Name: {name}")

    tx_power = getattr(advertisement, "tx_power", None)
    if tx_power is not None:
        print(f"TX Power: {tx_power} dBm")

    if connectable:
        print("Status: Connectable")
    else:
        print("Status: Discoverable")


def scan_bluetooth_devices(radio):
    """Scan for Bluetooth devices."""
    print("Starting Bluetooth scan...")
    print("Press Ctrl+C to stop")
    print("=" * 50)

    print(f"Adapter address: {format_address(getattr(radio, 'address', None))}")

    discovered = {}

    try:
        for scan_number in range(max_scans):
            print(f"\nScan {scan_number + 1}/{max_scans} - scanning for devices...")

            try:
                for advertisement in radio.start_scan(timeout=scan_interval):
                    key = format_address(getattr(advertisement, "address", None))
                    if key not in discovered:
                        discovered[key] = advertisement
                        print_advertisement(key, advertisement)
            finally:
                # Always stop the current scan before starting the next cycle
                radio.stop_scan()

            print(f"Found {len(discovered)} unique device(s) so far")

    except KeyboardInterrupt:
        print("\nStopping scan...")
        radio.stop_scan()

    # Summary
    print("\n" + "=" * 50)
    print("SCAN SUMMARY")
    print("=" * 50)
    print(f"Total unique devices found: {len(discovered)}")

    if discovered:
        print("\nDevices (sorted by signal strength):")
        sorted_devices = sorted(
            discovered.items(),
            key=lambda item: getattr(item[1], "rssi", -999) or -999,
            reverse=True,
        )
        for i, (address_str, advertisement) in enumerate(sorted_devices, 1):
            name = get_name(advertisement) or "Unknown"
            connectable = getattr(advertisement, "connectable", None)
            device_type = classify_device(get_name(advertisement), connectable)
            rssi = format_rssi(getattr(advertisement, "rssi", None))
            print(f"{i:2d}. {address_str} - {name} ({device_type}) - {rssi}")
    else:
        print("No devices found. Make sure nearby devices are advertising and in range.")

    print("\nBluetooth scan complete")


def test_bluetooth_capabilities(radio):
    """Perform a quick capability test."""
    print("Testing Bluetooth capabilities...")
    print(f"Adapter address: {format_address(getattr(radio, 'address', None))}")

    try:
        count = 0
        for _ in radio.start_scan(timeout=1):
            count += 1
            if count >= 3:
                break
        radio.stop_scan()
        print(f"Scan functionality working: found {count} device(s) in test")
        print("Bluetooth capabilities test passed")
        return True
    except Exception as e:
        print(f"Scan functionality issue: {e}")
        return False


# Main execution
try:
    radio = BLERadio()
except Exception as e:
    print(f"Error: could not initialize Bluetooth adapter: {e}")
    raise SystemExit

if test_mode:
    test_bluetooth_capabilities(radio)
else:
    scan_bluetooth_devices(radio)
