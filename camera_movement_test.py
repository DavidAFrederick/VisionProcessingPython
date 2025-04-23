
###  NOT COMPLETED

from gpiozero import Servo
import time
from sshkeyboard import listen_keyboard, stop_listening

# Install SSHKeyboard on RPI5:

# python3  -m venv /home/a/python
# ./pip3 install sshkeyboard


        # Define the GPIO pin number in BCM terms
        # This is physical Pin 7 on the left side just above the ground
MAGNETIC_SENSOR_PIN = 4
HEADING_MOTOR_PIN = 18    # was 17

global_key = "-"

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

class SecurityCamera():

    def __init__(self) -> None:

        self.initialize_pwm_motor()
        self.initialize_heading_motor_sensor()

    def initialize_pwm_motor(self) -> None:
        print ("Initializing pwm_motor - ", end=" ")
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(HEADING_MOTOR_PIN, GPIO.OUT)
        # pwm_motor = GPIO.PWM(HEADING_MOTOR_PIN, 50)  # channel=2 frequency=50Hz


        pwm_motor.start(6.6)
        max_speed = 84/10
        min_speed = 56/10
        pwm_motor.ChangeDutyCycle(6.6)   # Set motor to stopped
        print ("Done")
        # return pwm_motor
        
    def initialize_heading_motor_sensor(self) -> None:        
        print ("Initializing Heading sensor - ", end=" ")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(MAGNETIC_SENSOR_PIN, GPIO.IN, GPIO.PUD_UP)
        print ("Done")

    def monitor_magnetic_limit_switch(self)  -> bool:
        mag_switch = GPIO.input(MAGNETIC_SENSOR_PIN)
        return mag_switch
    
    def turn_heading_motor_until_limit(self, direction : str, allowed_duration = 12):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(HEADING_MOTOR_PIN, GPIO.OUT)
        pwm_motor = GPIO.PWM(HEADING_MOTOR_PIN, 50)  # channel=2 frequency=50Hz

        if (direction == "CW"):
            pwm_motor.start(8.4) # CW from top   
        if (direction == "CCW"):
            pwm_motor.start(5.6)    # CCV from top

        start_time = time.time()
        run_time = 0

        time.sleep(0.5)
        limit_switch_valid = self.monitor_magnetic_limit_switch()
        time_not_exceeded = run_time < allowed_duration

        while (limit_switch_valid) and (time_not_exceeded):
            if (direction == "CW"):
                pwm_motor.start(8.4)    # CW from top   
            if (direction == "CCW"):
                pwm_motor.start(5.6)    # CCV from top
            
            # print(f"Duration: {run_time:.2f}  Limit_switch: {self.monitor_magnetic_limit_switch()}  dir: {direction} " )

            time.sleep(0.1)
            run_time = time.time() - start_time
            limit_switch_valid = self.monitor_magnetic_limit_switch()
            time_not_exceeded = run_time < allowed_duration

        if (not limit_switch_valid):
            print ("Motion Limit detected")

        if (not time_not_exceeded):
                print ("Time Complete")

        pwm_motor.ChangeDutyCycle(6.6)   
        pwm_motor.stop()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


    def cleanup_GPIO(self):
        # led.cleanup()
        GPIO.cleanup()
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
            print ("Move Left for 1 second")
            security_camera.turn_heading_motor_until_limit("CCW", 1)

        if (global_key == "r") or (global_key == "right"):
            print ("Move Right for 1 second")
            security_camera.turn_heading_motor_until_limit("CW", 1)

        if (global_key == "q"):
            done = True

    security_camera.cleanup_GPIO()
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

if __name__ == "__main__":
    main()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 



