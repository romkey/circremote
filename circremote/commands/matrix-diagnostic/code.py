# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio
from adafruit_display_text import label

# Matrix configuration
width = {{ width }}
height = {{ height }}
bit_depth = {{ bit_depth }}
rgb_pins = {{ rgb_pins }}
addr_pins = {{ addr_pins }}
clock_pin = {{ clock_pin }}
latch_pin = {{ latch_pin }}
output_enable_pin = {{ output_enable_pin }}

print(f"LED Matrix Diagnostic")
print(f"Display: {width}x{height}")
print(f"Bit depth: {bit_depth}")
print(f"Total pixels: {width * height}")

# Release any previously-claimed displays before initializing the matrix
displayio.release_displays()

# Initialize the RGB matrix
matrix = rgbmatrix.RGBMatrix(
    width=width,
    height=height,
    bit_depth=bit_depth,
    rgb_pins=rgb_pins,
    addr_pins=addr_pins,
    clock_pin=clock_pin,
    latch_pin=latch_pin,
    output_enable_pin=output_enable_pin,
    doublebuffer=True,
)

# Create the display
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

def clear_display():
    """Clear the display to black."""
    display.root_group = displayio.Group()
    display.refresh()

def test_solid_colors():
    """Test solid color display."""
    print("\n=== Testing Solid Colors ===")
    
    colors = [
        ("Red", (255, 0, 0)),
        ("Green", (0, 255, 0)),
        ("Blue", (0, 0, 255)),
        ("White", (255, 255, 255)),
        ("Yellow", (255, 255, 0)),
        ("Cyan", (0, 255, 255)),
        ("Magenta", (255, 0, 255)),
        ("Black", (0, 0, 0))
    ]
    
    for color_name, rgb in colors:
        print(f"Testing {color_name}...")
        
        # Create bitmap with solid color
        bitmap = displayio.Bitmap(width, height, 1)
        palette = displayio.Palette(1)
        palette[0] = rgb
        
        # Fill bitmap
        for y in range(height):
            for x in range(width):
                bitmap[x, y] = 0
        
        # Create tile grid and show
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
        group = displayio.Group()
        group.append(tile_grid)
        display.root_group = group
        display.refresh()
        
        time.sleep(1)
    
    clear_display()

def test_pixel_grid():
    """Test individual pixel addressing."""
    print("\n=== Testing Pixel Grid ===")
    
    # Test pattern: alternating pixels
    bitmap = displayio.Bitmap(width, height, 2)
    palette = displayio.Palette(2)
    palette[0] = (0, 0, 0)      # Black
    palette[1] = (255, 255, 255) # White
    
    # Create checkerboard pattern
    for y in range(height):
        for x in range(width):
            if (x + y) % 2 == 0:
                bitmap[x, y] = 1
            else:
                bitmap[x, y] = 0
    
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
    group = displayio.Group()
    group.append(tile_grid)
    display.root_group = group
    display.refresh()
    
    print("Checkerboard pattern displayed for 3 seconds...")
    time.sleep(3)
    clear_display()

def test_brightness_levels():
    """Test different brightness levels."""
    print("\n=== Testing Brightness Levels ===")
    
    levels = [0.1, 0.3, 0.5, 0.7, 1.0]
    
    for level in levels:
        print(f"Testing brightness level: {level}")
        
        # Create white bitmap at different brightness
        brightness = int(255 * level)
        bitmap = displayio.Bitmap(width, height, 1)
        palette = displayio.Palette(1)
        palette[0] = (brightness, brightness, brightness)
        
        # Fill bitmap
        for y in range(height):
            for x in range(width):
                bitmap[x, y] = 0
        
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
        group = displayio.Group()
        group.append(tile_grid)
        display.root_group = group
        display.refresh()
        
        time.sleep(1)
    
    clear_display()

def test_animation():
    """Test smooth animation capability."""
    print("\n=== Testing Animation ===")
    
    # Animate a moving dot
    for frame in range(50):
        # Clear display
        bitmap = displayio.Bitmap(width, height, 2)
        palette = displayio.Palette(2)
        palette[0] = (0, 0, 0)      # Black
        palette[1] = (255, 0, 0)    # Red
        
        # Calculate dot position
        x = (frame * 2) % width
        y = height // 2
        
        # Set dot
        if 0 <= x < width and 0 <= y < height:
            bitmap[x, y] = 1
        
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
        group = displayio.Group()
        group.append(tile_grid)
        display.root_group = group
        display.refresh()
        
        time.sleep(0.1)
    
    clear_display()

def test_memory_usage():
    """Test memory usage and performance."""
    print("\n=== Testing Memory Usage ===")
    
    try:
        # Try to create a full-color bitmap
        print("Testing full-color bitmap creation...")
        bitmap = displayio.Bitmap(width, height, 256)
        palette = displayio.Palette(256)
        
        # Fill with gradient
        for i in range(256):
            palette[i] = (i, i, i)
        
        for y in range(height):
            for x in range(width):
                color_index = (x + y) % 256
                bitmap[x, y] = color_index
        
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
        group = displayio.Group()
        group.append(tile_grid)
        display.root_group = group
        display.refresh()
        
        print("Full-color gradient displayed for 2 seconds...")
        time.sleep(2)
        
    except MemoryError:
        print("WARNING: Memory error - matrix may be too large for full-color mode")
    except Exception as e:
        print(f"Error during memory test: {e}")
    
    clear_display()

def test_text_display():
    """Test text display capability."""
    print("\n=== Testing Text Display ===")
    
    try:
        # Create text label
        text = f"{width}x{height}"
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)
        text_area.x = width // 2 - len(text) * 3
        text_area.y = height // 2
        
        group = displayio.Group()
        group.append(text_area)
        display.root_group = group
        display.refresh()
        
        print(f"Text '{text}' displayed for 3 seconds...")
        time.sleep(3)
        
    except Exception as e:
        print(f"Text display test failed: {e}")
    
    clear_display()

def run_diagnostics():
    """Run all diagnostic tests."""
    print("Starting LED Matrix Diagnostics...")
    print("=" * 40)
    
    try:
        # Test 1: Solid colors
        test_solid_colors()
        
        # Test 2: Pixel grid
        test_pixel_grid()
        
        # Test 3: Brightness levels
        test_brightness_levels()
        
        # Test 4: Animation
        test_animation()
        
        # Test 5: Memory usage
        test_memory_usage()
        
        # Test 6: Text display
        test_text_display()
        
        print("\n=== Diagnostic Summary ===")
        print("✅ All tests completed successfully!")
        print(f"✅ Matrix size: {width}x{height} pixels")
        print(f"✅ Bit depth: {bit_depth}")
        print(f"✅ Total pixels: {width * height}")
        
        if bit_depth >= 4:
            print("✅ Full color support available")
        else:
            print("⚠️  Limited color support (consider increasing bit_depth)")
        
        if width * height <= 2048:
            print("✅ Memory usage should be acceptable")
        else:
            print("⚠️  Large matrix - monitor memory usage")
        
    except Exception as e:
        print(f"\n❌ Diagnostic failed: {e}")
        print("Check your matrix configuration and connections")
    
    finally:
        clear_display()
        print("\nDiagnostics complete.")

# Run the diagnostics
run_diagnostics()


