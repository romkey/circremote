# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import board
import pwmio

# Pin configuration
pin = {{ pin }}
frequency = {{ frequency }}
duty_cycle = {{ duty_cycle }}
mode = "{{ mode }}"
continuous = "{{ continuous }}".lower() in ("true", "1", "yes", "on")

print(f"PWM Write")
print(f"Pin: {pin}")
print(f"Frequency: {frequency} Hz")
print(f"Duty Cycle: {duty_cycle}%")

# Initialize PWM output
pwm = pwmio.PWMOut(pin, frequency=frequency, duty_cycle=0)

def set_pwm_duty_cycle(percent):
    """Set PWM duty cycle as a percentage."""
    try:
        # Convert percentage to 16-bit value (0-65535)
        duty_value = int((percent / 100.0) * 65535)
        
        # Clamp to valid range
        duty_value = max(0, min(65535, duty_value))
        
        # Set the duty cycle
        pwm.duty_cycle = duty_value
        
        print(f"Set PWM duty cycle to {percent}% (value: {duty_value})")
        
        return True
        
    except Exception as e:
        print(f"Error setting PWM duty cycle: {e}")
        return False

def set_pwm_frequency(freq):
    """Set PWM frequency by recreating the PWM output."""
    global pwm
    try:
        # Preserve the current duty cycle before deinit
        current_duty = pwm.duty_cycle
        pwm.deinit()
        pwm = pwmio.PWMOut(pin, frequency=freq, duty_cycle=current_duty)
        
        print(f"Set PWM frequency to {freq} Hz")
        
        return True
        
    except Exception as e:
        print(f"Error setting PWM frequency: {e}")
        return False

def fade_pwm(start_percent, end_percent, duration, steps=100):
    """Fade PWM from start to end percentage over duration."""
    print(f"Fading PWM from {start_percent}% to {end_percent}% over {duration}s...")
    
    try:
        step_delay = duration / steps
        step_size = (end_percent - start_percent) / steps
        
        for i in range(steps + 1):
            current_percent = start_percent + (step_size * i)
            set_pwm_duty_cycle(current_percent)
            time.sleep(step_delay)
        
        print("Fade complete")
        
    except Exception as e:
        print(f"Error during fade: {e}")

def sweep_pwm(start_percent, end_percent, duration, cycles=1):
    """Sweep PWM back and forth between start and end percentages."""
    print(f"Sweeping PWM from {start_percent}% to {end_percent}% ({cycles} cycles)...")
    
    try:
        for cycle in range(cycles):
            print(f"Cycle {cycle + 1}/{cycles}")
            
            # Fade up
            fade_pwm(start_percent, end_percent, duration / 2, 50)
            
            # Fade down
            fade_pwm(end_percent, start_percent, duration / 2, 50)
        
        print("Sweep complete")
        
    except Exception as e:
        print(f"Error during sweep: {e}")

def stop_pwm():
    """Stop PWM output (set duty cycle to 0)."""
    print("Stopping PWM output...")
    set_pwm_duty_cycle(0)

# Perform the PWM operation
if mode == "fade":
    fade_pwm({{ fade_start }}, {{ fade_end }}, {{ fade_duration }}, {{ fade_steps }})
elif mode == "sweep":
    sweep_pwm({{ sweep_start }}, {{ sweep_end }}, {{ sweep_duration }}, {{ sweep_cycles }})
elif mode == "stop":
    stop_pwm()
else:
    # Default: set duty cycle
    set_pwm_duty_cycle(duty_cycle)
    
    # If continuous mode, hold the value
    if continuous:
        print("PWM running continuously...")
        print("Press Ctrl+C to stop")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping PWM...")
            stop_pwm()
            print("PWM stopped.")

