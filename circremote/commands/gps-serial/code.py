# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import busio

# GPS configuration (pins are named from the board's perspective)
tx = {{ tx }}
rx = {{ rx }}
baud_rate = {{ baud }}

print(f"GPS Serial Reader")
print(f"Board TX Pin (to GPS RX): {tx}")
print(f"Board RX Pin (from GPS TX): {rx}")
print(f"Baud Rate: {baud_rate}")

# Initialize UART for GPS: busio.UART(tx, rx) uses the board's TX/RX pins
uart = busio.UART(tx, rx, baudrate=baud_rate)

def validate_checksum(sentence):
    """Validate an NMEA checksum. Returns True if valid or absent."""
    if '*' not in sentence:
        # No checksum present; nothing to validate against
        return True

    body, _, checksum = sentence[1:].partition('*')
    calculated = 0
    for char in body:
        calculated ^= ord(char)

    try:
        return calculated == int(checksum[:2], 16)
    except ValueError:
        return False


def parse_nmea_sentence(sentence):
    """Parse NMEA sentence and extract relevant data."""
    if not sentence.startswith('$'):
        return None

    if not validate_checksum(sentence):
        return None

    # Remove checksum and split by comma
    parts = sentence.split('*')[0].split(',')

    if not parts or len(parts[0]) < 6:
        return None

    # Strip the two-character talker ID (GP, GN, GL, ...) so multi-constellation
    # receivers that emit $GNGGA etc. are handled the same as $GPGGA.
    sentence_type = parts[0][3:]

    if sentence_type == 'GGA':
        # Global Positioning System Fix Data
        return parse_gga(parts)
    elif sentence_type == 'RMC':
        # Recommended Minimum Specific GPS/Transit Data
        return parse_rmc(parts)
    elif sentence_type == 'GLL':
        # Geographic Position - Latitude/Longitude
        return parse_gll(parts)
    elif sentence_type == 'GSV':
        # GPS Satellites in View
        return parse_gsv(parts)
    elif sentence_type == 'GSA':
        # GPS DOP and Active Satellites
        return parse_gsa(parts)

    return None

def parse_gga(parts):
    """Parse GGA sentence (Global Positioning System Fix Data)."""
    if len(parts) < 15:
        return None
    
    try:
        data = {
            'type': 'GGA',
            'time': parts[1] if parts[1] else None,
            'latitude': parts[2] if parts[2] else None,
            'lat_direction': parts[3] if parts[3] else None,
            'longitude': parts[4] if parts[4] else None,
            'lon_direction': parts[5] if parts[5] else None,
            'quality': parts[6] if parts[6] else None,
            'satellites': parts[7] if parts[7] else None,
            'hdop': parts[8] if parts[8] else None,
            'altitude': parts[9] if parts[9] else None,
            'altitude_units': parts[10] if parts[10] else None,
            'geoid_height': parts[11] if parts[11] else None,
            'geoid_units': parts[12] if parts[12] else None,
            'dgps_age': parts[13] if parts[13] else None,
            'dgps_id': parts[14] if parts[14] else None
        }
        
        # Convert coordinates to decimal degrees
        if data['latitude'] and data['lat_direction']:
            data['lat_decimal'] = convert_coordinate(data['latitude'], data['lat_direction'])
        if data['longitude'] and data['lon_direction']:
            data['lon_decimal'] = convert_coordinate(data['longitude'], data['lon_direction'])
        
        return data
    except (ValueError, IndexError):
        return None

def parse_rmc(parts):
    """Parse RMC sentence (Recommended Minimum Specific GPS/Transit Data)."""
    if len(parts) < 12:
        return None
    
    try:
        data = {
            'type': 'RMC',
            'time': parts[1] if parts[1] else None,
            'status': parts[2] if parts[2] else None,
            'latitude': parts[3] if parts[3] else None,
            'lat_direction': parts[4] if parts[4] else None,
            'longitude': parts[5] if parts[5] else None,
            'lon_direction': parts[6] if parts[6] else None,
            'speed': parts[7] if parts[7] else None,
            'course': parts[8] if parts[8] else None,
            'date': parts[9] if parts[9] else None,
            'magnetic_variation': parts[10] if parts[10] else None,
            'variation_direction': parts[11] if parts[11] else None
        }
        
        # Convert coordinates to decimal degrees
        if data['latitude'] and data['lat_direction']:
            data['lat_decimal'] = convert_coordinate(data['latitude'], data['lat_direction'])
        if data['longitude'] and data['lon_direction']:
            data['lon_decimal'] = convert_coordinate(data['longitude'], data['lon_direction'])
        
        return data
    except (ValueError, IndexError):
        return None

def parse_gll(parts):
    """Parse GLL sentence (Geographic Position - Latitude/Longitude)."""
    if len(parts) < 7:
        return None
    
    try:
        data = {
            'type': 'GLL',
            'latitude': parts[1] if parts[1] else None,
            'lat_direction': parts[2] if parts[2] else None,
            'longitude': parts[3] if parts[3] else None,
            'lon_direction': parts[4] if parts[4] else None,
            'time': parts[5] if parts[5] else None,
            'status': parts[6] if parts[6] else None
        }
        
        # Convert coordinates to decimal degrees
        if data['latitude'] and data['lat_direction']:
            data['lat_decimal'] = convert_coordinate(data['latitude'], data['lat_direction'])
        if data['longitude'] and data['lon_direction']:
            data['lon_decimal'] = convert_coordinate(data['longitude'], data['lon_direction'])
        
        return data
    except (ValueError, IndexError):
        return None

def parse_gsv(parts):
    """Parse GSV sentence (GPS Satellites in View)."""
    if len(parts) < 4:
        return None
    
    try:
        data = {
            'type': 'GSV',
            'total_sentences': parts[1] if parts[1] else None,
            'sentence_number': parts[2] if parts[2] else None,
            'satellites_in_view': parts[3] if parts[3] else None
        }
        
        # Parse satellite data (up to 4 satellites per sentence)
        satellites = []
        for i in range(4):
            sat_index = 4 + (i * 4)
            if sat_index + 3 < len(parts):
                if parts[sat_index]:  # PRN number exists
                    satellite = {
                        'prn': parts[sat_index],
                        'elevation': parts[sat_index + 1],
                        'azimuth': parts[sat_index + 2],
                        'snr': parts[sat_index + 3]
                    }
                    satellites.append(satellite)
        
        data['satellites'] = satellites
        return data
    except (ValueError, IndexError):
        return None

def parse_gsa(parts):
    """Parse GSA sentence (GPS DOP and Active Satellites)."""
    if len(parts) < 18:
        return None
    
    try:
        data = {
            'type': 'GSA',
            'mode': parts[1] if parts[1] else None,
            'fix_type': parts[2] if parts[2] else None,
            'satellites_used': []
        }
        
        # Parse satellite PRN numbers (up to 12)
        for i in range(12):
            sat_index = 3 + i
            if sat_index < len(parts) and parts[sat_index]:
                data['satellites_used'].append(parts[sat_index])
        
        # Parse DOP values
        if len(parts) > 15:
            data['pdop'] = parts[15] if parts[15] else None
        if len(parts) > 16:
            data['hdop'] = parts[16] if parts[16] else None
        if len(parts) > 17:
            data['vdop'] = parts[17] if parts[17] else None
        
        return data
    except (ValueError, IndexError):
        return None

def convert_coordinate(coord_str, direction):
    """Convert NMEA coordinate format to decimal degrees."""
    if not coord_str or not direction:
        return None
    
    try:
        # NMEA format: DDMM.MMMM or DDDMM.MMMM
        coord_float = float(coord_str)
        
        # Extract degrees and minutes
        degrees = int(coord_float // 100)
        minutes = coord_float % 100
        
        # Convert to decimal degrees
        decimal_degrees = degrees + (minutes / 60.0)
        
        # Apply direction (S or W = negative)
        if direction in ['S', 'W']:
            decimal_degrees = -decimal_degrees
        
        return decimal_degrees
    except (ValueError, TypeError):
        return None

def format_coordinate(decimal_degrees, is_latitude=True):
    """Format decimal degrees as human-readable coordinate."""
    if decimal_degrees is None:
        return "N/A"
    
    direction = 'N' if is_latitude else 'E'
    if decimal_degrees < 0:
        direction = 'S' if is_latitude else 'W'
        decimal_degrees = abs(decimal_degrees)
    
    return f"{decimal_degrees:.6f}° {direction}"

def print_gps_data(data):
    """Print formatted GPS data."""
    if not data:
        return
    
    print(f"\n--- {data['type']} Data ---")
    
    if data['type'] == 'GGA':
        print(f"Time: {data['time'] or 'N/A'}")
        print(f"Position: {format_coordinate(data.get('lat_decimal'), True)}, {format_coordinate(data.get('lon_decimal'), False)}")
        print(f"Quality: {data['quality'] or 'N/A'} ({'Fix' if data['quality'] == '1' else 'No Fix' if data['quality'] == '0' else 'Unknown'})")
        print(f"Satellites: {data['satellites'] or 'N/A'}")
        print(f"HDOP: {data['hdop'] or 'N/A'}")
        print(f"Altitude: {data['altitude'] or 'N/A'} {data['altitude_units'] or ''}")
    
    elif data['type'] == 'RMC':
        print(f"Time: {data['time'] or 'N/A'}")
        print(f"Date: {data['date'] or 'N/A'}")
        print(f"Status: {data['status'] or 'N/A'} ({'Valid' if data['status'] == 'A' else 'Invalid' if data['status'] == 'V' else 'Unknown'})")
        print(f"Position: {format_coordinate(data.get('lat_decimal'), True)}, {format_coordinate(data.get('lon_decimal'), False)}")
        print(f"Speed: {data['speed'] or 'N/A'} knots")
        print(f"Course: {data['course'] or 'N/A'}°")
    
    elif data['type'] == 'GLL':
        print(f"Position: {format_coordinate(data.get('lat_decimal'), True)}, {format_coordinate(data.get('lon_decimal'), False)}")
        print(f"Time: {data['time'] or 'N/A'}")
        print(f"Status: {data['status'] or 'N/A'} ({'Valid' if data['status'] == 'A' else 'Invalid' if data['status'] == 'V' else 'Unknown'})")
    
    elif data['type'] == 'GSV':
        print(f"Satellites in view: {data['satellites_in_view'] or 'N/A'}")
        print(f"Sentence {data['sentence_number'] or 'N/A'} of {data['total_sentences'] or 'N/A'}")
        if data.get('satellites'):
            print("Satellite details:")
            for sat in data['satellites']:
                print(f"  PRN {sat['prn']}: Elevation {sat['elevation']}°, Azimuth {sat['azimuth']}°, SNR {sat['snr']} dB")
    
    elif data['type'] == 'GSA':
        fix_types = {'1': 'No Fix', '2': '2D Fix', '3': '3D Fix'}
        print(f"Fix type: {data['fix_type'] or 'N/A'} ({fix_types.get(data['fix_type'], 'Unknown')})")
        print(f"Mode: {data['mode'] or 'N/A'}")
        print(f"Satellites used: {', '.join(data['satellites_used']) if data['satellites_used'] else 'N/A'}")
        print(f"PDOP: {data.get('pdop', 'N/A')}")
        print(f"HDOP: {data.get('hdop', 'N/A')}")
        print(f"VDOP: {data.get('vdop', 'N/A')}")

def read_gps_data():
    """Read and parse GPS data from serial connection."""
    print("Reading GPS data...")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    buffer = ""
    last_print_time = 0
    print_interval = {{ print_interval }}  # seconds
    
    try:
        while True:
            # Read data from UART
            if uart.in_waiting > 0:
                data = uart.read(uart.in_waiting)
                if data:
                    # Convert bytes to string and add to buffer
                    buffer += ''.join([chr(b) for b in data])
                    
                    # Process complete sentences
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        line = line.strip()
                        
                        if line:
                            # Parse NMEA sentence
                            gps_data = parse_nmea_sentence(line)
                            
                            # Print data at specified interval
                            current_time = time.monotonic()
                            if gps_data and (current_time - last_print_time) >= print_interval:
                                print_gps_data(gps_data)
                                last_print_time = current_time
            
            # Small delay to prevent excessive CPU usage
            time.sleep(0.01)
            
    except KeyboardInterrupt:
        print("\nStopping GPS reader...")
        print("GPS reader stopped.")

# Start reading GPS data
read_gps_data()

