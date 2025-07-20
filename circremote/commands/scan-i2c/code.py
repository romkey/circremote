# SPDX-FileCopyrightText: 2025 John Romkey 
#
# SPDX-License-Identifier: CC0-1.0

try:
    import board
    import busio
    from microcontroller import pin

    print("I2C module available")
except:
    print("No I2C support available")
    exit()

try:
    i2c = busio.I2C({{ scl }}, {{ sda }})
except:
    i2c = board.I2C()
    
print("Scanning I2C bus...")
        
devices = []

i2c.try_lock()
devices = i2c.scan()
i2c.unlock()
            
if devices:
    print(f"Found {len(devices)} I2C devices:")
    for i, addr in enumerate(devices, 1):
        print(f"{i}. Address: 0x{addr:02X} (decimal: {addr})")
else:
    print("No I2C devices found")
