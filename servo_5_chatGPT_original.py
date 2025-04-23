import gpiod
import time

# Constants
CHIP = "/dev/gpiochip0"
LINE_OFFSET = 18  # GPIO pin number (BCM numbering, e.g., GPIO18)
PERIOD = 0.02  # 20ms period typical for servo
MIN_PULSE = 0.0005  # 0.5 ms (0 degrees)
MAX_PULSE = 0.0025  # 2.5 ms (180 degrees)

# Helper: Map angle to pulse width
def angle_to_pulse(angle):
    return MIN_PULSE + (angle / 180.0) * (MAX_PULSE - MIN_PULSE)

# Open chip and request the GPIO line
chip = gpiod.Chip(CHIP)
line = chip.get_line(LINE_OFFSET)
line.request(consumer="servo", type=gpiod.LINE_REQ_DIR_OUT)

sleep_time = 3

try:
    while True:
        for angle in range(0, 181, 10):
            pulse_width = angle_to_pulse(angle)
            print(f"Angle: {angle}°, Pulse: {pulse_width:.4f}s")

            # Generate a single PWM pulse
            line.set_value(1)
            time.sleep(pulse_width)
            line.set_value(0)
            time.sleep(PERIOD - pulse_width)

        time.sleep(sleep_time)

        for angle in range(180, -1, -10):
            pulse_width = angle_to_pulse(angle)
            print(f"Angle: {angle}°, Pulse: {pulse_width:.4f}s")

            # Generate a single PWM pulse
            line.set_value(1)
            time.sleep(pulse_width)
            line.set_value(0)
            time.sleep(PERIOD - pulse_width)

        time.sleep(sleep_time)

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    line.set_value(0)
    line.release()
