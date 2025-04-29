# import numpy
import threading
import time
from sshkeyboard import listen_keyboard, stop_listening
import gpiod
from gpiod.line import Direction, Value

        # Define the GPIO pin number in BCM terms
        # This is physical Pin 7 on the left side just above the ground
MAGNETIC_SENSOR_PIN = 27
HEADING_MOTOR_PIN = 15

# Constants
CHIP = "/dev/gpiochip0"
PWM_LINE_OFFSET = 15 # 18 is busy  # GPIO pin number (BCM numbering, e.g., GPIO18)
SW_LINE_OFFSET = 27
LED_LINE_OFFSET = 14

PERIOD = 0.02  # 20ms period typical for servo
MIN_PULSE = 0.0005  # 0.5 ms (0 degrees)
MAX_PULSE = 0.0025  # 2.5 ms (180 degrees)

global_key = "-"
sleep_time = 0.1
angle = 0

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

class SecurityCamera():

    def __init__(self) -> None:

        self.initialize_chip()
        self.initialize_pwm_motor()
        self.initialize_heading_motor_sensor()
        self.last_motion_direction_that_was_permitted = None


    def initialize_chip(self) -> None:
        self.chip = gpiod.Chip(CHIP)
        self.value_str = {Value.ACTIVE: "Active", Value.INACTIVE: "Inactive"}
        self.value = Value.ACTIVE

    def initialize_pwm_motor(self) -> None:
        print ("Initializing pwm_motor - ", end=" ")
        self.pwm_line = gpiod.request_lines( CHIP,  config={PWM_LINE_OFFSET: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=self.value)})
        print ("Done")
        # return pwm_motor
        
    def initialize_heading_motor_sensor(self) -> None:        
        print ("Initializing Heading sensor - ", end=" ")
        self.switch_line = gpiod.request_lines( CHIP,  config={SW_LINE_OFFSET:  gpiod.LineSettings(direction=Direction.INPUT, bias=gpiod.line.Bias.PULL_UP)})
        print ("Done")

        # Helper: Map angle to pulse width
    def angle_to_pulse(self,angle):
        return MIN_PULSE + (angle / 180.0) * (MAX_PULSE - MIN_PULSE)

    def gpio_value_to_boolean(self, input_value) -> bool:
        if (input_value == Value.ACTIVE):
            return True
        return False

    def monitor_magnetic_limit_switch(self)  -> bool:
                # Read the switch status
        switch_status =  self.switch_line.get_value(SW_LINE_OFFSET)   
        boolean_switch_status =  self.gpio_value_to_boolean(switch_status)
        # print ("switch_status: ", boolean_switch_status, "    Raw: ", self.switch_line.get_value(SW_LINE_OFFSET))
        #
        # Limit switch is magnetic switch which connects pin to ground at limit.  Low = at limit
        # False = not at limit     // True = 

        return boolean_switch_status

    def turn_motor(self, speed : float, duration : float):

        #  Convert speed to pulse width.   
        # Where minimun pulse width = -100% motor speed
        #       maximum pulse width = +100% motor speed
        #  
        # MIN_PULSE + (angle / 180.0) * (MAX_PULSE - MIN_PULSE)
        # MIN_PULSE + (zero to one) x Change between (MAX_PULSE - MIN_PULSE)
        #
        # Sample Values:  
        # Speed value  | (zero to one) | pulse width  
        # -1.0 =               0.00
        # -0.5 =               0.25
        #  0.0 =               0.50
        # +0.5 =               0.75
        # +1.0 =               1.00
        #
        # Y = MX+B   = (1/2)X+0.5

        # pulse_width = self.angle_to_pulse(angle)
        # return MIN_PULSE + (angle / 180.0) * (MAX_PULSE - MIN_PULSE)

        pulse_width = MIN_PULSE + ((0.5 * speed) + 0.5) * (MAX_PULSE - MIN_PULSE)

        start_time = time.time()
        # print(f"Start:  {start_time}, Duration: {duration}     Speed: {speed},   Pulse: {pulse_width:.4f}s  PERIOD: {PERIOD}")

        while (time.time() - start_time < duration):
            print (f"Moving:  {speed}    limit switch ok to move {self.monitor_magnetic_limit_switch()}")
            # Generate a single PWM pulse.  Set high for duration of pulse width
            self.pwm_line.set_value(PWM_LINE_OFFSET,Value.ACTIVE)
            time.sleep(pulse_width)
            # Set low for the rest of the period interval
            self.pwm_line.set_value(PWM_LINE_OFFSET,Value.INACTIVE)
            time.sleep(PERIOD - pulse_width)

        # print(f"Stop:  {time.time()}")


    def turn_heading_motor_checking_limit(self, direction : str, speed = 0.2, allowed_duration = 1):
     
        # start_time = time.time()
        # run_time = 0
        # self.last_motion_direction_that_was_permitted = None
        limit_switch_valid  = True
        print (f"Before:  {self.monitor_magnetic_limit_switch()}  last dir: {self.last_motion_direction_that_was_permitted}  dir: {direction}")

        if (not self.monitor_magnetic_limit_switch()):  # Limit switch indicates at limit, only allow movement in the away from limit direction
            if (self.last_motion_direction_that_was_permitted == direction):  # If we're trying to move in the same direction that failed, prevent
                limit_switch_valid = False
                print ("Limit switch at limit - Trying to drive into the same direction that failed")
            else:
                limit_switch_valid = True
                print ("Limit switch at limit - OK to move in opposite direction")

        run_time = 0
        time_not_exceeded  = True
        duration = 0.25  # was 0.5
        start_time = time.time()

        while (limit_switch_valid) and (time_not_exceeded):    # Move in multiple small bursts
            if (direction == "CW"):
                self.turn_motor(speed, duration)  #  speed : float, allowed_duration : float)

            if (direction == "CCW"):
                self.turn_motor(-speed, duration)  #  speed : float, allowed_duration : float)
            
            run_time = time.time() - start_time
            time_not_exceeded = run_time < allowed_duration
            limit_switch_valid = self.monitor_magnetic_limit_switch()
            print(f"After:: Duration: {run_time:.2f}  Speed {speed:.2f}  Limit_switch: {limit_switch_valid}  dir: {direction} " )
            self.last_motion_direction_that_was_permitted = direction

        if (not limit_switch_valid):
            print ("Motion Limit detected")

        if (not time_not_exceeded):
                print ("Time Complete")

        self.turn_motor(0.0, 0.0)    # Stop the motor
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


    def cleanup_GPIO(self):

        self.pwm_line.set_value(PWM_LINE_OFFSET,Value.INACTIVE)
        self.pwm_line.release()
        # self.LED_line.set_value(LED_LINE_OFFSET,Value.INACTIVE)
        # self.LED_line.release()

        self.switch_line.release()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

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
def main():
    security_camera = SecurityCamera()
    done = False



    while (not done):

        print_header()
        
        listen_keyboard(on_press = read_key_press,)

        if (global_key == "l") or (global_key == "left"):
            # print (f"Move Left for {} second")
            security_camera.turn_heading_motor_checking_limit("CCW", 0.25, 0.5)

        if (global_key == "r") or (global_key == "right"):
            # print ("Move Right for 1 second")
            security_camera.turn_heading_motor_checking_limit("CW", 0.25, 0.5)

        if (global_key == "q"):
            done = True

    security_camera.cleanup_GPIO()
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

if __name__ == "__main__":
    main()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 



