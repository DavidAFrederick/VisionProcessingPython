from sshkeyboard import listen_keyboard, stop_listening
import gpiod
import time
from gpiod.line import Direction, Value


# https://libgpiod.readthedocs.io/en/latest/python_api.html

# Constants
CHIP = "/dev/gpiochip0"
PWM_LINE_OFFSET = 15 # 18 is busy  # GPIO pin number (BCM numbering, e.g., GPIO18)
SW_LINE_OFFSET = 14
LED_LINE_OFFSET = 27

PERIOD = 0.02  # 20ms period typical for servo
MIN_PULSE = 0.0005  # 0.5 ms (0 degrees)
MAX_PULSE = 0.0025  # 2.5 ms (180 degrees)

# PERIOD = 2  # 20ms period typical for servo  ##### ADDED
# MIN_PULSE = 0.5  # 0.5 ms (0 degrees)
# MAX_PULSE = 1.5  # 2.5 ms (180 degrees)

# Helper: Map angle to pulse width
def angle_to_pulse(angle):
    return MIN_PULSE + (angle / 180.0) * (MAX_PULSE - MIN_PULSE)

# Open chip and request the GPIO line
chip = gpiod.Chip(CHIP)


line = chip.get_line_info(PWM_LINE_OFFSET)
# line = chip.get_line(PWM_LINE_OFFSET)

value_str = {Value.ACTIVE: "Active", Value.INACTIVE: "Inactive"}
value = Value.ACTIVE

# line.request(consumer="servo", type=gpiod.LINE_REQ_DIR_OUT)
line = gpiod.request_lines( CHIP,  config={PWM_LINE_OFFSET: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=value)})

sleep_time = 0.1
angle = 0

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
global_key = "-"

def read_key_press(key):
    global global_key
    global_key = key
    stop_listening()

def print_header():
    print ("=================================")
    print ("Move Left for one second  = l ")
    print ("Move Right for one second = r ")
    print ("Quit = q")
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Examples:
##  https://github.com/brgl/libgpiod/tree/master/bindings/python/examples

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

try:
    while True:
        print ("Pin to be used: ", PWM_LINE_OFFSET)
        print_header()
        listen_keyboard(on_press = read_key_press,)

        if (global_key == "up"):
            print ("Up key pressed")
            angle = angle + 30

        if (global_key == "down"):
            print ("Down key pressed")
            angle = angle - 30

        if (global_key == "l") or (global_key == "left"):
            print ("Move Left for 1 second")

        if (global_key == "r") or (global_key == "right"):
            print ("Move Right for 1 second")

        if (global_key == "q"):
            done = True
            break

        pulse_width = angle_to_pulse(angle)
        print(f"Angle: {angle}°, Pulse: {pulse_width:.4f}s")

        for counter in range(10):

            # Generate a single PWM pulse
            # line.set_value(1)
            line.set_value(PWM_LINE_OFFSET,Value.ACTIVE)
            time.sleep(pulse_width)

            # line.set_value(0)
            line.set_value(PWM_LINE_OFFSET,Value.INACTIVE)
            time.sleep(PERIOD - pulse_width)

        time.sleep(sleep_time)

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    # line.set_value(0)
    line.set_value(PWM_LINE_OFFSET,Value.INACTIVE)
    line.release()
