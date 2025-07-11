# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

try:
    import board
    import busio

    print("I2C module available")
    
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
    except Exception as e:

        from microcontroller import pin

#        sda_pin = pin.Pin({sda})
#        scl_pin = pin.Pin({scl})
        sda_pin = pin.GPIO17
        scl_pin = pin.GPIO18
        i2c = busio.I2C(scl_pin, sda_pin)

#        print(f"Using custom pins: SDA=Pin({sda}), SCL=Pin({scl})")

        print(f"Error during scan: {e}")

        i2c = busio.I2C(board.SCL, board.SDA)
        print(f"Using default board pins: SDA={board.SDA}, SCL={board.SCL}")
    
    print("Scanning I2C bus...")
        
    devices = []
    try:
       i2c.try_lock()
try:
       devices = i2c.scan()
       i2c.unlock()
    except Exception as e:
except Exception as e:    print(f"Error initializing scan-i2c: {e}")    import sys    sys.exit(1)        print(f"Error during scan: {e}")
            
    if devices:
        print(f"Found {len(devices)} I2C devices:")
        for i, addr in enumerate(devices, 1):
            print(f"{i}. Address: 0x{addr:02X} (decimal: {addr})")
                
            if addr == 0x3C or addr == 0x3D:
                print("   Likely: SSD1306 OLED Display")
            elif addr == 0x68:
                print("   Likely: DS3231 RTC or MPU6050 Accelerometer")
            elif addr == 0x76 or addr == 0x77:
                print("   Likely: BME280/BMP280 Temperature/Pressure Sensor")
            elif addr == 0x23 or addr == 0x5C:
                print("   Likely: BH1750 Light Sensor")
            elif addr == 0x48 or addr == 0x49:
                print("   Likely: ADS1115 ADC")
            elif addr >= 0x20 and addr <= 0x27:
                print("   Likely: PCF8574/MCP23017 I/O Expander")
            else:
                print("   Device type: Unknown")
    else:
        print("No I2C devices found")
            
except Exception as e:
    print(f"Error setting up I2C: {e}")
except ImportError:
    print("I2C module not available on this device")
except Exception as e:
    print(f"Error accessing I2C module: {e}")
