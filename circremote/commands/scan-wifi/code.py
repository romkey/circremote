# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

try:
    import wifi

    print("WiFi module available")
    
    try:
        networks = []
        print("Scanning for networks...")
        
        for network in wifi.radio.start_scanning_networks():
            ssid = network.ssid
            if not ssid:
                ssid = "(hidden network)"

            bssid = ":".join(["{:02x}".format(b) for b in network.bssid])
            rssi = network.rssi
            channel = network.channel
            security = str(network.authmode)
            networks.append((ssid, rssi, channel, bssid, security))
    except Exception as e:
        print(f"Error initializing scan_wifi: {e}")
        import sys
        sys.exit(1)        

    wifi.radio.stop_scanning_networks()
        
    networks.sort(key=lambda x: x[1], reverse=True)
        
    print(f"Found {len(networks)} networks:")
    for i, (ssid, rssi, channel, bssid, security) in enumerate(networks, 1):
        print(f"{i}. SSID: {ssid}")
        print(f": {rssi} dBm")
        print(f"   Channel: {channel}")
        print(f"   BSSID: {bssid}")
        print(f"   Security: {security}\n")
            
except ImportError:
    print("WiFi module not available on this device")
except Exception as e:
    print(f"Error accessing WiFi module: {str(e)}")
